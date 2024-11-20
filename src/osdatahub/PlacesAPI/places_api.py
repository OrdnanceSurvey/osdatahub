from collections.abc import Iterable
from typing import Union

import requests
from typeguard import typechecked

import osdatahub
from osdatahub import Extent
from osdatahub.grow_list import GrowList
from osdatahub.utils import addresses_to_geojson, validate_in_range
from osdatahub.codes import DATASET

class PlacesAPI:
    """Main class for querying the OS Places API (https://osdatahub.os.uk/docs/places/overview)

    Args:
        key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/

    Example::

        from osdatahub import PlacesAPI, Extent
        from os import environ

        key = environ.get("OS_API_KEY")
        places = PlacesAPI(key)
        extent = Extent.from_radius((437293, 115515), 800, "EPSG:27700")
        results = places.query(extent, limit=100)
    """

    __ENDPOINT = r"https://api.os.uk/search/places/v1/"
    HEADERS = {"method": "POST", "headers": "{'Content-Type': 'application/json'}"}

    def __init__(self, key: str):
        self.key = key

    def __endpoint(self, api_name: str) -> str:
        return self.__ENDPOINT + api_name + f"?key={self.key}"

    @staticmethod
    def __get_dataset_param(dataset: Union[str, Iterable] ) -> str:
        if not isinstance(dataset, str):
            dataset_unique = set(dataset)
            shared_datasets = dataset_unique & DATASET

            if len(shared_datasets) == len(dataset_unique):
                return ",".join(dataset_unique)

        elif  dataset in DATASET:
            return dataset

        raise ValueError(f"Unrecognised dataset, expected 'LPI', 'DPA' or ['LPI', 'DPA'], got {dataset}")

    @typechecked
    def query(
            self,
            extent: Extent,
            output_crs: str = None,
            limit: int = 100,
            classification_code: Union[str, Iterable, None] = None,
            logical_status_code: Union[str, int, None] = None,
            dataset: Union[str, Iterable, None] = None
    ) -> dict:
        """Run a query of the OS Places API within a given extent

        Args:
            extent (Extent): The geographical extent of your query
            output_crs (str, optional): The intended output CRS
            limit (int, optional): The maximum number of features to return.
                Defaults to 100.
            classification_code (str|Iterable[str], optional): Classification codes to filter query by
            logical_status_code (str|int, optional): logical status codes to filter query by
            dataset (str|Iterable, optional): The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        if not output_crs:
            output_crs = extent.crs
        data = GrowList()
        params = {
            "url": self.__endpoint("polygon"),
            "headers": self.HEADERS,
            "json": extent.to_json(),
            "params": {"srs": extent.crs, "output_srs": output_crs},
        }
        if classification_code or logical_status_code:
            params["params"].update(
                {"fq": self.__format_fq(classification_code, logical_status_code)}
            )

        if dataset is not None:
            params["params"].update(
                {"dataset": self.__get_dataset_param(dataset)}
            )

        try:
            n_required = min(limit, 100)
            while n_required > 0 and data.grown:
                params["params"].update({"offset": len(data), "maxresults": n_required})
                response = osdatahub.post(**params)
                data.extend(self.__format_response(response))
                n_required = min(100, limit - len(data))
        except KeyError:
            response.raise_for_status()
        return addresses_to_geojson(data.values, output_crs)

    @typechecked
    def find(
            self,
            text: str,
            output_crs: str = "EPSG:27700",
            limit: int = 100,
            classification_code: Union[str, Iterable, None] = None,
            logical_status_code: Union[str, int, None] = None,
            minmatch: Union[float, None] = None,
            matchprecision: Union[int, None] = None,
            dataset: Union[str, Iterable, None] = None
    ) -> dict:
        """A free text query of the OS Places API

        Args:
            text (str): The free text search parameter
            output_crs (str, optional): The intended output CRS
            limit (int, optional): The maximum number of features to return.
                Defaults to 100.
            classification_code (str|Iterable[str], optional): Classification codes to filter query by
            logical_status_code (str|int, optional): logical status codes to filter query by
            minmatch (float, optional): The minimum match score a result has to have to be returned
            matchprecision (int, optional): The decimal point position at which the match score value is to be truncated
            dataset (str|Iterable, optional): The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        data = GrowList()
        params = {"query": text, "output_srs": output_crs}
        if minmatch is not None:
            params["minmatch"] = validate_in_range(minmatch, 0.1, 1)
        if matchprecision is not None:
            params["matchprecision"] = str(validate_in_range(matchprecision, 1, 10))
        if classification_code or logical_status_code:
            params.update(
                {"fq": self.__format_fq(classification_code, logical_status_code)}
            )
        
        if dataset is not None:
            params.update(
                {"dataset": self.__get_dataset_param(dataset)}
            )

        try:
            n_required = min(limit, 100)
            while n_required > 0 and data.grown:
                params.update({"offset": len(data), "maxresults": n_required})
                response = osdatahub.get(self.__endpoint("find"), params=params, proxies=osdatahub.get_proxies())
                data.extend(self.__format_response(response))
                n_required = min(100, limit - len(data))
        except KeyError:
            response.raise_for_status()
        return addresses_to_geojson(data.values, output_crs)

    @typechecked
    def postcode(
            self,
            postcode: str,
            output_crs: str = "EPSG:27700",
            limit: int = 100,
            classification_code: Union[str, Iterable, None] = None,
            logical_status_code: Union[str, int, None] = None,
            dataset: Union[str, Iterable, None] = None
    ) -> dict:
        """A query based on a property’s postcode. The minimum for the
        resource is the area and district

        e.g. SO16, and will accept a full postcode consisting of the area,
        district, sector and unit e.g. SO16 0AS

        Args:
            postcode (str): The postcode search parameter
            output_crs (str, optional): The intended output CRS.
                Defaults to "EPSG:27700".
            limit (int, optional): The maximum number of features to return.
                Defaults to 100.
            classification_code (str|Iterable[str], optional): Classification codes to filter query by
            logical_status_code (str|int, optional): logical status codes to filter query by
            dataset (str|Iterable, optional): The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        data = GrowList()
        params = {"postcode": postcode, "output_srs": output_crs}
        if classification_code or logical_status_code:
            params.update(
                {"fq": self.__format_fq(classification_code, logical_status_code)}
            )
        if dataset is not None:
            params.update(
                {"dataset": self.__get_dataset_param(dataset)}
            )

        try:
            n_required = min(limit, 100)
            while n_required > 0 and data.grown:
                params.update({"offset": len(data), "maxresults": n_required})
                response = osdatahub.get(self.__endpoint("postcode"), params=params, proxies=osdatahub.get_proxies())
                data.extend(self.__format_response(response))
                n_required = min(100, limit - len(data))
        except KeyError:
            response.raise_for_status()
        return addresses_to_geojson(data.values, output_crs)

    @typechecked
    def uprn(
            self,
            uprn: int,
            output_crs: str = "EPSG:27700",
            classification_code: Union[str, Iterable, None] = None,
            logical_status_code: Union[str, int, None] = None,
            dataset: Union[str, Iterable, None] = None
    ) -> dict:
        """A query that takes a UPRN as the search parameter

        Args:
            uprn (int): A Valid UPRN
            output_crs (str, optional): The intended output CRS.
                Defaults to "EPSG:27700".
            classification_code (str|Iterable[str], optional): Classification codes to filter query by
            logical_status_code (str|int, optional): logical status codes to filter query by
            dataset (str|Iterable, optional): The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        data = GrowList()
        params = {"uprn": uprn, "output_srs": output_crs}
        if classification_code or logical_status_code:
            params.update(
                {"fq": self.__format_fq(classification_code, logical_status_code)}
            )
        if dataset is not None:
            params.update(
                {"dataset": self.__get_dataset_param(dataset)}
            )
        try:
            response = osdatahub.get(self.__endpoint("uprn"), params=params, proxies=osdatahub.get_proxies())
            data.extend(self.__format_response(response))
        except KeyError:
            response.raise_for_status()
        return addresses_to_geojson(data.values, output_crs)

    @typechecked
    def nearest(
            self,
            point: tuple,
            point_crs: str,
            radius: float = 100,
            output_crs: str = "EPSG:27700",
            classification_code: Union[str, Iterable] = None,
            logical_status_code: Union[str, int] = None,
            dataset: Union[str, Iterable, None] = None
    ) -> dict:
        """Takes a pair of coordinates (X, Y)/(Lon, Lat) as an input
        to determine the closest address.

        Args:
            point (tuple): A set of coordinates
            point_crs (str): The crs corresponding to the point coordinates
            radius (float): The search radius in metres (max. 1000).
                Defaults to 100.
            output_crs (str, optional): The intended output CRS.
                Defaults to "EPSG:27700".
            classification_code (str|Iterable[str], optional): Classification codes to filter query by
            logical_status_code (str|int, optional): logical status codes to filter query by
            dataset (str|Iterable, optional): The dataset to return. Multiple values can be sent, separated by a comma. Default: DPA.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        data = GrowList()
        point = point if point_crs.upper() != "EPSG:4326" else (point[1], point[0])
        params = {
            "point": ",".join([str(c) for c in point]),
            "srs": point_crs,
            "output_srs": output_crs,
            "radius": radius,
        }
        if classification_code or logical_status_code:
            params.update(
                {"fq": self.__format_fq(classification_code, logical_status_code)}
            )
        if dataset is not None:
            params.update(
                {"dataset": self.__get_dataset_param(dataset)}
            )
        try:
            response = osdatahub.get(self.__endpoint("nearest"), params=params, proxies=osdatahub.get_proxies())
            data.extend(self.__format_response(response))
        except KeyError:
            response.raise_for_status()
        return addresses_to_geojson(data.values, output_crs)

    @staticmethod
    def __format_response(response: requests.Response) -> list:
        results = response.json()["results"]
        return [result[list(result.keys())[0]] for result in results]

    @staticmethod
    @typechecked
    def __format_fq(
            classification_code: Union[str, Iterable, None] = None,
            logical_status_code: Union[str, int, None] = None,
    ) -> list:
        """
        Formats optional fq arguments for Places API query

        Args:
            classification_code (str|Iterable[str], optional): The classification codes to filter query
            logical_status_code (str|Number, optional): Logical status code to filter query

        Returns:
            list of fq filtering arguments
        """
        fq_args = []
        if classification_code:
            if isinstance(classification_code, str):
                class_codes = "classification_code:" + classification_code
            elif isinstance(classification_code, Iterable):
                class_codes = " ".join(
                    [f"classification_code:{arg}" for arg in classification_code]
                )
            else:
                raise TypeError(
                    f"'classification_code' argument must be Iterable or str, but was type {type(classification_code)}"
                )

            fq_args.append(class_codes)
        if logical_status_code:
            if not str(logical_status_code).isnumeric():
                raise TypeError(
                    "logical_status_code can have a maximum of 1 filter and must have a numeric value."
                )

            fq_args.append("logical_status_code:" + str(logical_status_code))

        return fq_args


if __name__ == "__main__":
    from os import environ

    key = environ.get("OS_API_KEY")
    places = PlacesAPI(key)

    # extent = Extent.from_bbox((-3.2939550711619177,50.746391786819316,-3.2788419310229244,50.75566426785872), "EPSG:4326")
    # results = places.query(extent, limit=42)
    results = places.find(
        "Ordnance Survey Adanac Drive SO16",
        minmatch=0.4,
        matchprecision=9
    )
    # places.nearest((-3.2939550711619177,50.746391786819316), "EPSG:4326", 1000)

    print(results)
    # import json

    # with open("test.json", "w") as f:
    #     json.dump(results, f)
