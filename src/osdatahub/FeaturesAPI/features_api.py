import json
import warnings

import requests
from geojson import FeatureCollection
from typeguard import typechecked

import osdatahub
from osdatahub.extent import Extent
from osdatahub.errors import raise_http_error
from osdatahub.FeaturesAPI.feature_products import (get_product,
                                                    validate_product_name)
from osdatahub.filters import Filter
from osdatahub.grow_list import GrowList
from osdatahub.spatial_filter_types import SpatialFilterTypes
from osdatahub.utils import features_to_geojson, is_new_api

class FeaturesAPI:
    """Main class for querying the OS Features API (https://osdatahub.os.uk/docs/wfs/overview)

    Args:
        key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/
        product_name (str): A valid OS product
        extent (Extent): The geographical extent of your query
        spatial_filter_type (str): Set the default spatial filter operation (defaults to "intersects")

    Example::

        from osdatahub import FeaturesAPI, Extent
        from os import environ

        key = environ.get("OS_API_KEY")
        extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")
        features = FeaturesAPI(key, "zoomstack_local_buildings", extent)
        results = features.query(limit=50)
    """

    ENDPOINT = r"https://api.os.uk/features/v1/wfs"

    DEFAULTS = {
        "service": "wfs",
        "version": "2.0.0",
        "request": "GetFeature",
        "outputFormat": "geojson",
        "count": 100,
    }

    def __init__(self, key: str, product_name: str, extent: Extent, spatial_filter_type: str = "intersects"):
        self.key: str = key
        self.new_api: bool = False
        self.product: str = product_name
        self.extent: Extent = extent
        self.filters: list = []
        self.__spatial_filter = SpatialFilterTypes.get(spatial_filter_type)

    @property
    def extent(self):
        return self.__extent

    @extent.setter
    def extent(self, o: object):
        if isinstance(o, Extent):
            self.__extent = o
        else:
            o_type = type(o)
            raise TypeError(
                f'type of argument "extent" must be '
                f"osdatahub.extent.Extent; got {o_type} instead"
            )

    @property
    def product(self):
        return self.__product

    @product.setter
    def product(self, product_name: str):
        product_name = validate_product_name(product_name)
        self.__product = get_product(product_name, self.new_api)
        self.__product_name = product_name

    @property
    def xml_filter(self):
        return self.__construct_filter()

    @typechecked
    def query(self, limit: int = 100) -> FeatureCollection:
        """Run a query of the OS Features API

        Args:
            limit (int, optional): The maximum number of features to return.
                Defaults to 100.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """

        params = self.__params
        data = GrowList()
        n_required = min(limit, 100)
        if "srsName='EPSG:4326'" in params["filter"]:
            warnings.warn("The features API does not support EPSG:4326 and will return an empty features list.")

        try:
            while n_required > 0 and data.grown:
                params.update({"count": n_required, "startIndex": len(data)})
                response = osdatahub.get(self.ENDPOINT, params=params, proxies=osdatahub.get_proxies())
                resp_json = response.json()
                if "fault" in resp_json:
                    raise_http_error(response)
                if is_new_api(resp_json):
                    self.new_api = True
                    self.product = self.__product_name
                data.extend(resp_json["features"])
                n_required = min(100, limit - len(data))
        except json.decoder.JSONDecodeError:
            raise_http_error(response)

        if data and not is_new_api(data):
            warnings.warn("The OS Data Hub has updated the Features API, fixing some important bugs and adding some "
                          "new properties to all responses.\nTo access these features, consider regenerating your API "
                          "key in the OS Data Hub API dashboard.\nMore information about the update can be found at"
                          "osdatahub.os.uk.", DeprecationWarning)
        return features_to_geojson(data.values, self.product.geometry,
                                   self.extent.crs)

    def __construct_filter(self) -> str:
        filter_body = self.__spatial_filter(self.extent)
        for _filter in self.filters:
            filter_body += _filter
            filter_body = f"<ogc:And>{filter_body}</ogc:And>"
        return f"<ogc:Filter>{filter_body}</ogc:Filter>"

    @property
    def __params(self) -> dict:
        return {
            **self.DEFAULTS,
            "key": self.key,
            "srsName": self.extent.crs,
            "typeName": self.product.name,
            "filter": self.__construct_filter(),
        }
    
    @typechecked
    def add_filters(self, *xml_filters: Filter) -> None:
        """Add XML filter strings to the final query

        Args:
            xml_filters (str): Valid OGC XML filter objects
        """
        
        self.filters.extend(xml_filters)


if __name__ == "__main__":
    from os import environ

    from osdatahub import Extent, FeaturesAPI

    key = environ.get("OS_API_KEY")

    bbox = (-1.5339625, 53.787380, -1.5266132, 53.794103)
    extent = Extent.from_bbox(bbox, "EPSG:4326")

    product = "Zoomstack_Sites"
    features = FeaturesAPI(key, product, extent, spatial_filter_type="equals")
    results = features.query()

    print(len(results["features"]))
