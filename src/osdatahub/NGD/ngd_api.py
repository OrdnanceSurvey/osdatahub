import functools
import json
import logging
from datetime import datetime
from typing import Union

import requests
from typeguard import typechecked

import osdatahub
from osdatahub import Extent
from osdatahub.NGD.crs import get_crs


def _merge_geojsons(gj1: Union[dict], gj2: Union[dict]) -> Union[dict]:
    """
    Combines 2 geojsons from NGD api into a single valid geojson

    Args:
        gj1 (FeatureCollection): A FeatureCollection
        gj2 (FeatureCollection): Another FeatureCollection

    Returns (FeatureCollection): A FeatureCollection with a single set of Features and a combined numberReturned

    """
    if not (gj1 or gj2):
        raise ValueError("Inputs were both empty")
    elif not gj1:
        return gj2
    elif not gj2:
        return gj1

    required_keys = {"features", "numberReturned", "links"}
    if not (gj1.keys() >= required_keys and gj2.keys() >= required_keys):
        raise ValueError(f"Both geojsons must contain keys {required_keys}")

    merged_geojson = gj1.copy()
    merged_geojson["features"] = merged_geojson["features"] + gj2["features"]
    merged_geojson["numberReturned"] += gj2["numberReturned"]
    merged_geojson["links"] += gj2["links"]

    return merged_geojson


class NGD:
    """
    Main class for querying OS NGD Features API (https://osdatahub.os.uk/docs/ofa/overview)

    Args:
        key (str): A valid OS Data Hub API key. Get a free key here - https://osdatahub.os.uk/
        collection (str): ID for the desired NGD Feature Collection. Learn about the possible collection ids here -
            https://osdatahub.os.uk/docs/ofa/technicalSpecification

    Example::

        from osdatahub import NGD
        from os import environ

        key = environ.get("OS_API_KEY")
        extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")
        features = NGD(key, "bld-fts-buildingline")
        results = features.query(max_results=50, extent=extent)
    """
    __ENDPOINT = r"https://api.os.uk/features/ngd/ofa/v1/collections"

    __HEADERS = {'Accept': 'application/geo+json'}

    def __init__(self, key: str, collection: str):
        self.key: str = key
        self.collection: str = collection

    def __endpoint(self, feature_id=None) -> str:
        return f"{self.__ENDPOINT}/{self.collection}/items/{feature_id if feature_id else ''}"

    @classmethod
    @functools.lru_cache()
    def get_collections(cls) -> dict:
        """
        Retrieves all OS NGD Feature Collections
        Returns:
            Dict: Dictionary containing all Feature Collections currently supported with details for each
        """
        response = osdatahub.get(cls.__ENDPOINT, proxies=osdatahub.get_proxies())
        response.raise_for_status()
        return response.json()
    
    @typechecked
    def query(self,
              extent: Union[Extent, None] = None,
              crs: Union[str, int, None] = None,
              start_datetime: Union[datetime, None] = None,
              end_datetime: Union[datetime, None] = None,
              cql_filter: Union[str, None] = None,
              filter_crs: Union[str, int, None] = None,
              max_results: int = 100,
              offset: int = 0) -> Union[dict]:
        """
        Retrieves features from a Collection

        Args:
            extent (Extent, optional): An extent, either from a bounding box or a Polygon. Only features within this
                extent will be returned
                Available CRS values are: EPSG:27700, EPSG:4326, EPSG:3857, and CRS84. Defaults to CRS84
            crs (str|int, optional): The CRS for the returned features, either in the format "epsg:xxxx" or an epsg
                number. e.g. British National Grid can be supplied as "epsg:27700" or 27700.
                Available CRS values are: EPSG:27700, EPSG:4326, EPSG:7405, EPSG:3857, and CRS84. Defaults to CRS84
            start_datetime (datetime, optional): Selects features that have a temporal property after the given start
                time. If you want to query a single timestamp, provide the same value to both start_datetime
                and end_datetime
            end_datetime (datetime, optional): Selects features that have a temporal property before the given end
                time. If you want to query a single timestamp, provide the same value to both start_datetime
                and end_datetime
            cql_filter (str, optional): A filter query in the CQL format. More information about supported CQL operators
                can be found at https://osdatahub.os.uk/docs/ofa/technicalSpecification
            filter_crs (str|int, optional): The CRS for a given CQL query, either in the format "epsg:xxxx" or an epsg
                number. e.g. British National Grid can be supplied as "epsg:27700" or 27700
                Available CRS values are: EPSG:27700, EPSG:4326, EPSG:7405, EPSG:3857, and CRS84. Defaults to CRS84
            max_results (int, optional): The maximum number of features to return. Defaults to 100
            offset (int, optional): The offset number skips past the specified number of features in the collection.
                Defaults to 0

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """

        assert max_results > 0, f"Argument max_results must be greater than 0 but was {max_results}"
        assert offset >= 0, f"Argument offset must be greater than 0 but was {offset}"
        params = {}

        # Checking validity and preformatting arguments
        if crs:
            params["crs"] = get_crs(crs=crs)

        if start_datetime or end_datetime:
            if start_datetime and end_datetime and start_datetime > end_datetime:
                raise ValueError("Start time must be before end time")

            start_datetime = start_datetime.isoformat() + "Z" if start_datetime else ".."
            end_datetime = end_datetime.isoformat() + "Z" if end_datetime else ".."

            params["datetime"] = f"{start_datetime}/{end_datetime}"

        if extent:
            bbox_filter = f"INTERSECTS(geometry, {extent.polygon.wkt})"

            # ADD INTERSECTS QUERY
            if cql_filter:
                if filter_crs:
                    assert get_crs(extent.crs, valid_crs=("epsg:4326", "epsg:27700", "epsg:3857", "crs84")) == \
                           get_crs(filter_crs), "If passing extent and a cql filter with a crs, the filter_crs must " \
                                                "be same as the extent crs"
                else:
                    filter_crs = extent.crs

                cql_filter += f" AND {bbox_filter}"
            else:
                cql_filter = bbox_filter
                filter_crs = extent.crs

        if cql_filter:
            params['filter'] = cql_filter
            if filter_crs:
                params['filter-crs'] = get_crs(crs=filter_crs, valid_crs=("epsg:4326", "epsg:27700", "epsg:3857",
                                                                          "crs84"))

        n_required = max_results

        data = {}

        headers = self.__HEADERS
        headers.update({"key": self.key})

        while n_required > 0:
            limit = min(n_required, 100)
            offset = max(offset, data["numberReturned"] if "numberReturned" in data else 0)
            params.update({"limit": limit, "offset": offset})
            try:
                response = osdatahub.get(self.__endpoint(), params=params, headers=headers, proxies=osdatahub.get_proxies())
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(json.dumps(e.response.json(), indent=4))
                raise e

            resp_json = response.json()
            data = _merge_geojsons(data, resp_json)

            if resp_json["numberReturned"] < limit:
                break
            else:
                n_required -= resp_json["numberReturned"]

        return data

    def query_feature(self, feature_id: str, crs: Union[str, int] = None) -> dict:
        """
        Retrieves a single feature from a collection

        Args:
            feature_id: An identifier ID for a feature
            crs (str|int, optional): The CRS for the returned feature, either in the format "epsg:xxxx" or an epsg
                number. e.g. British National Grid can be supplied as "epsg:27700" or 27700.
                Available CRS values are: EPSG:27700, EPSG:4326, EPSG:7405, EPSG:3857, and CRS84. Defaults to CRS84

        Returns:
            Feature: A GeoJSON Feature containing the requested feature
        """
        params = {"crs": get_crs(crs)} if crs else {}

        response = osdatahub.get(self.__endpoint(feature_id), params=params, headers={"key": self.key}, proxies=osdatahub.get_proxies())
        response.raise_for_status()

        return response.json()
