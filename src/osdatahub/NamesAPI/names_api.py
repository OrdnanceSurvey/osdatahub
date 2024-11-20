from collections.abc import Iterable
from typing import Union

from typeguard import typechecked

import osdatahub
from osdatahub.errors import raise_http_error
from osdatahub.extent import Extent
from osdatahub.grow_list import GrowList
from osdatahub.NamesAPI.local_types import get_local_type, validate_local_type
from osdatahub.utils import addresses_to_geojson


class NamesAPI:
    """Main class for querying the OS Names API (https://osdatahub.os.uk/docs/names/overview)

    Args:
        key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/

    Example::

        from osdatahub import NamesAPI
        from os import environ

        key = environ.get("OS_API_KEY")
        names = NamesAPI(key)
        results = names.find("Buckingham Palace", limit=5)
    """
    __ENDPOINT = r"https://api.os.uk/search/names/v1/"
    HEADERS = {"method": "POST",
               "headers": "{'Content-Type': 'application/json'}"}

    def __init__(self, key: str):
        self.key = key

    def __endpoint(self, api_name: str) -> str:
        return self.__ENDPOINT + api_name + f"?key={self.key}"

    @typechecked
    def find(self,
             text: str,
             limit: int = 100,
             bounds: Union[Extent, None] = None,
             bbox_filter: Union[Extent, None] = None,
             local_type: Union[Iterable, str, None] = None) -> dict:
        """A free text query of the OS Names API

        Args:
            text (str): The free text search parameter
            limit (int, optional): The maximum number of features to return.
                Defaults to 100.
            bounds (Extent, optional): Biases the results to a certain area. Must be British National Grid
                (EPSG:27700) CRS
            bbox_filter (Extent, optional): Filters the results to a certain area. Must be British National Grid
                (EPSG:27700) CRS
            local_type (Union[Iterable, str], optional): Filters the results to certain local types. Available local
                types can be found at the bottom of https://osdatahub.os.uk/docs/names/technicalSpecification

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        data = GrowList()
        params = {"query": text}

        if limit <= 0:
            raise ValueError(f"Parameter \"limit\" must be a positive integer. Instead got {limit}")

        if bounds:
            if not bounds.crs == "EPSG:27700":
                raise TypeError("Bounds must be in British National Grid CRS (EPSG:27700)")
            params.update({"bounds": bounds.bbox.to_string(precision=2)})
        if bbox_filter or local_type:
            if bbox_filter and (not bbox_filter.crs == "EPSG:27700"):
                raise TypeError("Bounding Box filter must be in British National Grid CRS (EPSG:27700)")
            params.update({"fq": self.__format_fq(bbox_filter, local_type)})

        try:
            n_required = min(limit, 100)
            while n_required > 0 and data.grown:
                params.update({"offset": len(data), "maxresults": n_required})
                response = osdatahub.get(self.__endpoint("find"), params=params, proxies=osdatahub.get_proxies())
                data.extend(self.__format_response(response))
                n_required = min(100, limit - len(data))
        except KeyError:
            raise_http_error(response)
        return addresses_to_geojson(data.values, "EPSG:27700")

    @typechecked
    def nearest(self,
                point: tuple,
                radius: float = 100,
                local_type: Union[Iterable, str, None] = None) -> dict:
        """Takes a pair of coordinates (X, Y) as an input
        to determine the closest name.

        Args:
            point (tuple): A set of coordinates in British National Grid (EPSG:27700) format
            radius (float): The search radius in metres (min. 0.01, max. 1000).
                Defaults to 100.
            local_type (Union[Iterable, str], optional):  Filters the results to certain local types. Available local
                types can be found at the bottom of https://osdatahub.os.uk/docs/names/technicalSpecification

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        data = GrowList()
        if not all([str(p).isnumeric() for p in point]):
            raise TypeError("All values in argument \"point\" must be numeric")
        if not 0.01 <= radius <= 1000:
            raise ValueError(f"Argument \"radius\" must be between 0.01 and 1000, but had value {radius}")

        params = {"point": ",".join([str(c) for c in point]), "radius": radius}
        if local_type:
            params.update({"fq": self.__format_fq(local_type=local_type)})
        try:
            response = osdatahub.get(self.__endpoint("nearest"), params=params, proxies=osdatahub.get_proxies())
            data.extend(self.__format_response(response))
        except KeyError:
            if response.status_code != 200:
                raise_http_error(response)
        return addresses_to_geojson(data.values, crs="EPSG:27700")

    @staticmethod
    @typechecked
    def __format_fq(bbox_filter: Union[Extent, None] = None,
                    local_type: Union[str, Iterable, None] = None) -> list:
        """
        Formats optional fq arguments for Names API query

        Args:
            bbox_filter (Extent, optional): Filters the results to a certain area. Must be British National Grid
                (EPSG:27700) CRS
            local_type (Union[str, Iterable], optional): Filters the results to certain local types. Available local
                types can be found at the bottom of https://osdatahub.os.uk/docs/names/technicalSpecification

        Returns:
            list of fq filtering arguments
        """
        fq_args = []
        if local_type:
            # check that all given local types are valid
            invalid_local_types = validate_local_type(local_type)
            if invalid_local_types:
                raise ValueError(f"The local type(s) {invalid_local_types} are not valid local types")
            # builds local_type query whether given one argument or multiple
            if isinstance(local_type, str):
                local_types = "LOCAL_TYPE:" + get_local_type(local_type)
            elif isinstance(local_type, Iterable):
                local_types = " ".join([f"LOCAL_TYPE:{get_local_type(arg)}" for arg in local_type])
            else:
                raise TypeError(
                    f"'local_type' argument must be Iterable or str, but was type {type(local_type)}")
            fq_args.append(local_types)

        # adds bbox filter to argument
        if bbox_filter:
            if not bbox_filter.crs == "EPSG:27700":
                raise ValueError("'bbox_filter' argument must have CRS of British National Grid (EPSG:27700). Its CRS "
                                 f"is {bbox_filter.crs}")
            fq_args.append("BBOX:" + str(bbox_filter.bbox.to_string(precision=2)))

        return fq_args

    @staticmethod
    def __format_response(response) -> list:
        try:
            return [result["GAZETTEER_ENTRY"] for result
                    in response.json()["results"]]
        except KeyError as e:
            if response.status_code == 200:
                    return []
            raise e