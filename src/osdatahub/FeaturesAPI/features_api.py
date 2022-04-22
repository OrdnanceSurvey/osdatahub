import json

import requests
from geojson import FeatureCollection
from osdatahub.errors import raise_http_error
from osdatahub import Extent
from osdatahub.FeaturesAPI import feature_products as products
from osdatahub.FeaturesAPI.feature_products import get_product, validate_product_name
from osdatahub.filters import intersects
from osdatahub.grow_list import GrowList
from osdatahub.utils import features_to_geojson
from typeguard import typechecked


class FeaturesAPI:
    """Main class for querying the OS Features API (https://osdatahub.os.uk/docs/wfs/overview)

    Args:
        key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/
        product_name (str): A valid OS product
        extent (Extent): The geographical extent of your query

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

    def __init__(self, key: str, product_name: str, extent: Extent):
        self.key = key
        self.product = product_name
        self.extent = extent
        self.filters = []

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
        self.__product = get_product(product_name)

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
        try:
            while n_required > 0 and data.grown:
                params.update({"count": n_required, "startIndex": len(data)})
                response = requests.get(self.ENDPOINT, params=params)
                data.extend(response.json()["features"])
                n_required = min(100, limit - len(data))
        except json.decoder.JSONDecodeError:
            raise_http_error(response)
        return features_to_geojson(data.values, self.product.geometry,
                                   self.extent.crs)

    def __construct_filter(self) -> str:
        filter_body = intersects(self.extent)
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
    def add_filters(self, *xml_filters: str) -> None:
        """Add XML filter strings to the final query

        Args:
            xml_filters (str): Valid OGC XML filter objects
        """
        for xml_filter in xml_filters:
            self.filters.append(xml_filter)


if __name__ == "__main__":
    from os import environ

    from osdatahub import Extent, FeaturesAPI
    import geojson

    key = environ.get("OS_API_KEY")

    bbox = (-1.1446, 52.6133, -1.0327, 52.6587)
    extent = Extent.from_bbox(bbox, "EPSG:4326")

    product = "Zoomstack_Sites"
    features = FeaturesAPI(key, product, extent)
    results = features.query()

    print(len(results["features"]))
