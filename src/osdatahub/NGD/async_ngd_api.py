import asyncio
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from typeguard import typechecked

import osdatahub
from osdatahub import Extent
from osdatahub.AsyncAPI import AsyncHTTPClient
from osdatahub.NGD.crs import get_crs
from osdatahub.NGD.models import FeatureCollection


# TODO: check that this is more efficient - avoids having to do the copy each time like the synchonous version
def _merge_all_geojsons(geojsons: List[Dict]) -> FeatureCollection:
    """Merge multiple GeoJSON FeatureCollections into one efficiently."""
    if not geojsons:
        raise ValueError("No geojsons to merge")

    required_keys = {"features", "numberReturned", "links"}
    for gj in geojsons:
        if not gj.keys() >= required_keys:
            raise ValueError(f"All geojsons must contain keys {required_keys}")

    base = geojsons[0]
    features = list(base.get("features", []))
    links = list(base.get("links", []))
    count = base.get("numberReturned", 0)

    for gj in geojsons[1:]:
        features.extend(gj.get("features", []))
        links.extend(gj.get("links", []))
        count += gj.get("numberReturned", 0)

    return FeatureCollection(
        type=base.get("type", "FeatureCollection"),
        features=features,
        numberReturned=count,
        links=links,
        timeStamp=base.get("timeStamp"),
        numberMatched=base.get("numberMatched"),
    )


class AsyncNGD:
    """
    Async client for querying OS NGD Features API.

    This class provides async methods for querying the OS National Geographic Database
    with support for parallel pagination, rate limiting, and automatic retries.

    Args:
        key: A valid OS Data Hub API key. Get a free key at https://osdatahub.os.uk/
        collection: ID for the desired NGD Feature Collection. See available collections at
            https://osdatahub.os.uk/docs/ofa/technicalSpecification
        max_concurrent: Maximum concurrent requests (default: 5)
        request_delay: Delay between requests in seconds (default: 0.3)
        max_retries: Maximum retry attempts on failure (default: 3)

    Example::

        from osdatahub import AsyncNGD, Extent
        import asyncio

        async def main():
            key = "your-api-key"
            extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")

            async with AsyncNGD(key, "trn-ntwk-street-1") as ngd:
                # Fetches 500 features in parallel (5 pages of 100)
                results = await ngd.query(max_results=500, extent=extent)
                print(f"Got {len(results['features'])} features")

        asyncio.run(main())
    """

    __ENDPOINT = r"https://api.os.uk/features/ngd/ofa/v1/collections"
    __HEADERS = {"Accept": "application/geo+json"}
    __PAGE_SIZE = 100  # NGD API max per request

    _collections_cache: Optional[Dict] = None

    def __init__(
        self,
        key: str,
        collection: str,
        max_concurrent: int = 5,
        request_delay: float = 0.02,  # could make this 0 but I think API limts would be hit
        max_retries: int = 3,
    ) -> None:
        self.key: str = key
        self.collection: str = collection
        self._client: Optional[AsyncHTTPClient] = None

        # Store config
        self._max_concurrent = max_concurrent
        self._request_delay = request_delay
        self._max_retries = max_retries

    def _get_client(self) -> AsyncHTTPClient:
        """Initialisation of HTTP client."""
        if self._client is None:
            self._client = AsyncHTTPClient(
                max_concurrent=self._max_concurrent,
                request_delay=self._request_delay,
                max_retries=self._max_retries,
                proxies=osdatahub.get_proxies(),
            )
        return self._client

    def _endpoint(self, feature_id: Optional[str] = None) -> str:
        """Build endpoint URL."""
        return f"{self.__ENDPOINT}/{self.collection}/items/{feature_id if feature_id else ''}"

    def _build_headers(self) -> Dict[str, str]:
        """Build request headers."""
        return self.__HEADERS.copy()

    def _add_auth(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Add API key to query parameters."""
        params = params.copy()
        params["key"] = self.key
        return params

    @classmethod
    async def get_collections(cls, client: Optional[AsyncHTTPClient] = None) -> Dict:
        """
        Async retrieval of all OS NGD Feature Collections.

        Args:
            client: Optional AsyncHTTPClient to use. If not provided,
                creates a temporary client that will be closed after the request.

        Returns:
            Dict containing all Feature Collections with details for each.
        """
        if cls._collections_cache is not None:
            return cls._collections_cache

        should_close = client is None
        if client is None:
            client = AsyncHTTPClient(proxies=osdatahub.get_proxies())

        try:
            result = await client.get(cls.__ENDPOINT)
            cls._collections_cache = result
            return result
        finally:
            if should_close:
                await client.close()

    @classmethod
    def clear_collections_cache(cls) -> None:
        """Clear the cached collections data."""
        cls._collections_cache = None

    @typechecked
    async def query(
        self,
        extent: Optional[Extent] = None,
        crs: Optional[Union[str, int]] = None,
        start_datetime: Optional[datetime] = None,
        end_datetime: Optional[datetime] = None,
        cql_filter: Optional[str] = None,
        filter_crs: Optional[Union[str, int]] = None,
        max_results: Optional[int] = 100,
        offset: int = 0,
    ) -> FeatureCollection:
        """
        Async query for features from a Collection with parallel pagination.

        This method will automatically paginate through results, fetching
        multiple pages in parallel for improved performance.

        Args:
            extent: An Extent object for spatial filtering. Only features within
                this extent will be returned. Supports EPSG:27700, EPSG:4326,
                EPSG:3857, and CRS84.
            crs: CRS for returned features. Can be "epsg:xxxx" format or EPSG code
                as int. Available: EPSG:27700, EPSG:4326, EPSG:7405, EPSG:3857, CRS84.
                Defaults to CRS84.
            start_datetime: Filter for features with temporal property after this time.
            end_datetime: Filter for features with temporal property before this time.
            cql_filter: A CQL format filter query. See OS docs for supported operators.
            filter_crs: CRS for the CQL query geometry. Must match extent CRS if both provided.
            max_results: Maximum number of features to return. Set to None to fetch all
                available features (default: 100).
            offset: Starting offset for pagination (default: 0).

        Returns:
            FeatureCollection with merged results.

        Raises:
            AssertionError: If max_results <= 0 or offset < 0.
            ValueError: If start_datetime > end_datetime or CRS validation fails.
        """
        if max_results is not None:
            assert max_results > 0, f"max_results must be > 0, got {max_results}"
        assert offset >= 0, f"offset must be >= 0, got {offset}"

        params = self._build_params(
            extent=extent,
            crs=crs,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            cql_filter=cql_filter,
            filter_crs=filter_crs,
        )

        client = self._get_client()
        headers = self._build_headers()

        # If max_results is None, fetch all available features
        # TODO: Could just default to this
        if max_results is None:
            return await self._fetch_all(client, params, headers, offset)

        # Calculate pagination for fixed max_results
        page_offsets = self._calculate_page_offsets(max_results, offset)

        tasks = []
        for page_offset, page_limit in page_offsets:
            page_params = {**params, "limit": page_limit, "offset": page_offset}
            tasks.append(self._fetch_page(client, page_params, headers))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        successful_results: List[Dict] = []
        for i, result in enumerate(results):
            if isinstance(result, BaseException):
                logging.error(
                    f"Page fetch failed for offset {page_offsets[i][0]}: {result}"
                )
                raise result
            page_result: Dict = result
            features_count = len(page_result.get("features", []))

            if features_count < page_offsets[i][1]:
                successful_results.append(page_result)
                break
            successful_results.append(page_result)

        # TODO: maybe raise exception instead?
        if not successful_results:
            return FeatureCollection(
                type="FeatureCollection",
                features=[],
                numberReturned=0,
                links=[],
            )

        return _merge_all_geojsons(successful_results)

    def _calculate_page_offsets(
        self, max_results: int, start_offset: int
    ) -> List[Tuple[int, int]]:
        """
        Calculate (offset, limit) tuples for parallel fetching.

        Args:
            max_results: Total number of results desired
            start_offset: Starting offset

        Returns:
            List of (offset, limit) tuples for each page to fetch
        """
        pages = []
        remaining = max_results
        current_offset = start_offset

        while remaining > 0:
            page_limit = min(remaining, self.__PAGE_SIZE)
            pages.append((current_offset, page_limit))
            current_offset += page_limit
            remaining -= page_limit

        return pages

    async def _fetch_page(
        self, client: AsyncHTTPClient, params: Dict, headers: Dict
    ) -> Dict:
        """Fetch a single page of results."""
        return await client.get(
            self._endpoint(), params=self._add_auth(params), headers=headers
        )

    async def _fetch_all(
        self,
        client: AsyncHTTPClient,
        params: Dict,
        headers: Dict,
        start_offset: int = 0,
    ) -> FeatureCollection:
        """
        Fetch all available features by paginating until no more results.
        """
        all_results: List[Dict] = []
        current_offset = start_offset
        batch_size = self._max_concurrent

        while True:
            tasks = []
            offsets = []
            for i in range(batch_size):
                offset = current_offset + (i * self.__PAGE_SIZE)
                offsets.append(offset)
                page_params = {**params, "limit": self.__PAGE_SIZE, "offset": offset}
                tasks.append(self._fetch_page(client, page_params, headers))

            results = await asyncio.gather(*tasks, return_exceptions=True)

            done = False
            for i, result in enumerate(results):
                if isinstance(result, BaseException):
                    logging.error(
                        f"Page fetch failed for offset {offsets[i]}: {result}"
                    )
                    raise result

                page_result: Dict = result
                features_count = len(page_result.get("features", []))

                if features_count > 0:
                    all_results.append(page_result)

                if features_count < self.__PAGE_SIZE:
                    done = True
                    break

            if done:
                break

            current_offset += batch_size * self.__PAGE_SIZE

        # TODO: Raise exception here?
        if not all_results:
            return FeatureCollection(
                type="FeatureCollection",
                features=[],
                numberReturned=0,
                links=[],
            )

        return _merge_all_geojsons(all_results)

    def _build_params(
        self,
        extent: Optional[Extent],
        crs: Optional[Union[str, int]],
        start_datetime: Optional[datetime],
        end_datetime: Optional[datetime],
        cql_filter: Optional[str],
        filter_crs: Optional[Union[str, int]],
    ) -> Dict[str, Any]:
        """Build query parameters (mirrors sync implementation logic)."""
        params: Dict[str, Any] = {}

        if crs:
            params["crs"] = get_crs(crs=crs)

        if start_datetime or end_datetime:
            if start_datetime and end_datetime and start_datetime > end_datetime:
                raise ValueError("Start time must be before end time")

            start_str = start_datetime.isoformat() + "Z" if start_datetime else ".."
            end_str = end_datetime.isoformat() + "Z" if end_datetime else ".."
            params["datetime"] = f"{start_str}/{end_str}"

        if extent:
            bbox_filter = f"INTERSECTS(geometry, {extent.polygon.wkt})"

            if cql_filter:
                if filter_crs:
                    assert get_crs(
                        extent.crs,
                        valid_crs=("epsg:4326", "epsg:27700", "epsg:3857", "crs84"),
                    ) == get_crs(filter_crs), "filter_crs must match extent crs"
                else:
                    filter_crs = extent.crs
                cql_filter += f" AND {bbox_filter}"
            else:
                cql_filter = bbox_filter
                filter_crs = extent.crs

        if cql_filter:
            params["filter"] = cql_filter
            if filter_crs:
                params["filter-crs"] = get_crs(
                    crs=filter_crs,
                    valid_crs=("epsg:4326", "epsg:27700", "epsg:3857", "crs84"),
                )

        return params

    async def query_feature(
        self, feature_id: str, crs: Optional[Union[str, int]] = None
    ) -> Dict:
        """
        Async retrieval of a single feature by ID.

        Args:
            feature_id: The unique identifier of the feature to retrieve.
            crs: CRS for the returned feature. Can be "epsg:xxxx" format or
                EPSG code as int. Defaults to CRS84.

        Returns:
            GeoJSON Feature object.
        """
        params = {"crs": get_crs(crs)} if crs else {}
        headers = self._build_headers()

        client = self._get_client()
        return await client.get(
            self._endpoint(feature_id), params=self._add_auth(params), headers=headers
        )

    async def close(self) -> None:
        """Close the HTTP client and release resources."""
        if self._client is not None:
            await self._client.close()
            self._client = None

    async def __aenter__(self) -> "AsyncNGD":
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Async context manager exit - cleanup."""
        await self.close()
