from ast import main
import json
from datetime import datetime
from os import environ
from typing import Union
import logging

import requests
from geojson import FeatureCollection
from typeguard import check_argument_types

from osdatahub import Extent
from osdatahub.NGDAPI.collections import validate_collection
from osdatahub.NGDAPI.crs import get_crs
#from crs import get_crs
from osdatahub.errors import raise_http_error


def merge_geojsons(gj1, gj2):
    if not (gj1 or gj2):
        raise ValueError("Inputs were both empty")
    elif not gj1:
        return gj2
    elif not gj2:
        return gj1

    gj1["features"] += gj2["features"]
    gj1["numberReturned"] += gj2["numberReturned"]
    gj1["links"] += gj2["links"]

    return gj1


class NGDAPI:
    __ENDPOINT = r"https://api.os.uk/features/ngd/ofa/v1/"

    DEFAULTS = {

    }

    def __init__(self, key: str, collection: str, extent: Extent = None):
        self.key: str = key
        self.collection: str = collection
        self.extent = extent

    @property
    def collection(self):
        return self.__collection

    @collection.setter
    def collection(self, col: str):
        col = validate_collection(col)
        self.__collection = col
        self.__collection_name = col

    def __endpoint(self, collection, feature_id=None) -> str:
        return f"{self.__ENDPOINT}/collections/{collection}/items/{feature_id if feature_id else ''}"

    def query(self,
              extent: Extent = None,
              crs: str = None,
              start_datetime: datetime = None,
              end_datetime: datetime = None,
              filter=None,
              filter_crs: Union[str, int] = None,
              limit: int = 100,
              offset: int = 0,
              epsg: int = None) -> FeatureCollection:

        assert check_argument_types()

        params = {}

        # Checking validity of arguments
        # Add arguments to params
        if crs or epsg:
            params["crs"] = get_crs(crs=crs, epsg=epsg)

        if extent:
            params["bbox"] = extent.bbox
            params["bbox-crs"] = get_crs(extent.crs, valid_crs=("epsg:4326", "epsg:27700", "epsg:3857", "crs84"))

        if start_datetime or end_datetime:
            if start_datetime and end_datetime and start_datetime > end_datetime:
                raise ValueError("Start time must be before end time")

            start_datetime = start_datetime.isoformat() + "Z" if start_datetime else ".."
            end_datetime = end_datetime.isoformat() + "Z" if end_datetime else ".."

            params["datetime"] = f"{start_datetime}/{end_datetime}"

        if filter:
            params['filter'] = filter

        if filter_crs:
            if filter == None: logging.warning("filter_crs ignored, filter not provided")
            elif isinstance(filter_crs,str):
                params['filter-crs'] = get_crs(crs=filter_crs, valid_crs=("epsg:4326", "epsg:27700", "epsg:3857", "crs84"))
            elif isinstance(filter_crs,int):
                params['filter-crs'] = get_crs(epsg=filter_crs, valid_crs=("epsg:4326", "epsg:27700", "epsg:3857", "crs84"))

        n_required = min(limit, 100)
        data = {}
        while n_required > 0:
            offset = max(offset, data["numberReturned"] if "numberReturned" in data else 0)
            params.update(
                {"limit": n_required, "offset": offset})
            try:
                response = requests.get(self.__endpoint(self.collection), params=params, headers={"key": self.key})
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(json.dumps(e.response.json(),indent=4))
                raise e

            resp_json = response.json()

            # if response.status_code != 200:
            #     if response.status_code == 400:
            #         raise ValueError(resp_json['description'])
            #     else:
            #         raise_http_error(response)

            data = merge_geojsons(data, resp_json)

            if resp_json["numberReturned"] < n_required:
                break
            else:
                n_required = min(100, limit - data["numberReturned"])

        return data
