import json
from os import environ

import geojson
import requests
from geojson import FeatureCollection
from typeguard import typechecked

import osdatahub
from osdatahub import Extent, FeaturesAPI
from osdatahub.errors import raise_http_error
from osdatahub.filters import is_equal
from osdatahub.grow_list import GrowList

"""
script to generate unprocessed API data
"""


class FeaturesAPI_NoPostProcessing(FeaturesAPI):
    @typechecked
    def query(self, limit: int = 1000) -> FeatureCollection:
        """Run a query of the OS Features API WITHOUT POST PROCESSING

        Args:
            limit (int, optional): The maximum number of features to return.
                Defaults to 1000.

        Returns:
            FeatureCollection: The results of the query in GeoJSON format
        """
        params = self._FeaturesAPI__params()
        data = GrowList()
        n_required = min(limit, 100)
        try:
            while n_required > 0 and data.grown:
                params.update({"count": n_required, "startIndex": len(data)})
                response = osdatahub.get(self.ENDPOINT, params=params, proxies=osdatahub.get_proxies())
                data.extend(response.json()["features"])
                n_required = min(100, limit - len(data))
        except json.decoder.JSONDecodeError:
            raise_http_error(response)
        # DOESN'T run features_to_geojson before returning result
        return FeatureCollection(data.values, crs=self.extent.crs)


def round_recursively(lst):
    if isinstance(lst, (float, int)):
        return round(lst, 2)
    else:
        return [round_recursively(i) for i in lst]


if __name__ == "__main__":

    # Need equivelant files via QGIS. Export features WITHOUT any properties.
    test_polygons = [
        (
            "osgb4000000073320773",
            (391436, 172360, 393874, 174833),
            "sites_multipolygon",
        ),
        (
            "osgb4000000073320772",
            (391436, 172360, 393874, 174833),
            "sites_polygon_with_hole",
        ),
        ("osgb4000000073320770", (391436, 172360, 393874, 174833), "sites_polygon"),
        (
            "osgb4000000073320769",
            (391436, 172360, 393874, 174833),
            "sites_multipolygon_with_hole",
        ),
        (
            "osgb4000000073495159",
            (336610, 503920, 338001, 505331),
            "sites_multipolygon2",
        ),
    ]

    key = environ.get("OS_API_KEY")
    folder = r"tests\data\clean_polygon_data\API (uncleaned)"
    for TOID, bbox, save_name in test_polygons:
        extent = Extent.from_bbox(bbox, "EPSG:27700")
        features = FeaturesAPI_NoPostProcessing(key, "sites_functional_site", extent)
        features.add_filters(is_equal("TOID", TOID))
        results = features.query(limit=42)

        for site in results["features"]:
            coords = site["geometry"]["coordinates"]
            site["geometry"]["coordinates"] = round_recursively(coords)
            site["properties"] = {}
        with open(rf"{folder}\{save_name}.geojson", "w", encoding="utf-8") as f:
            geojson.dump(
                FeatureCollection(results, crs="EPSG:27700"),
                f,
                ensure_ascii=False,
                indent=4,
            )
            print(f"{save_name} saved")
