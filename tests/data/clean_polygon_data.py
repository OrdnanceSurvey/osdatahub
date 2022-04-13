import geojson
from pytest import param
from shapely.geometry import MultiPolygon, Polygon, mapping


def test_clean_polygon():
    test_variables = "feature, expected_result"
    test_data = [
        param(
            {"geometry": simple_polygon1},
            {"geometry": simple_polygon1.copy()},
            id="simple polygon",
        ),
        param(
            {"geometry": simple_polygon2},
            {"geometry": simple_polygon2.copy()},
            id="simple polygon 2",
        ),
        param(
            {"geometry": polygon_with_hole},
            {"geometry": polygon_with_hole.copy()},
            id="polygon with hole",
        ),
        param(
            {"geometry": multipolygon1},
            {"geometry": multipolygon1.copy()},
            id="simple multipolygon",
        ),
        param(
            {"geometry": multipolygon_with_hole},
            {"geometry": multipolygon_with_hole.copy()},
            id="multipolygon with hole",
        ),
        param(
            {"geometry": get_test_polygons("sites_polygon", "API (uncleaned)")},
            {"geometry": get_test_polygons("sites_polygon", "QGIS")},
            id="sites polygon",
        ),
        param(
            {
                "geometry": get_test_polygons(
                    "sites_polygon_with_hole", "API (uncleaned)"
                )
            },
            {"geometry": get_test_polygons("sites_polygon_with_hole", "QGIS")},
            id="sites polygon with hole",
        ),
        param(
            {"geometry": get_test_polygons("sites_multipolygon", "API (uncleaned)")},
            {"geometry": get_test_polygons("sites_multipolygon", "QGIS")},
            id="sites multipolygon",
        ),
        param(
            {"geometry": get_test_polygons("sites_multipolygon2", "API (uncleaned)")},
            {"geometry": get_test_polygons("sites_multipolygon2", "QGIS")},
            id="sites multipolygon2",
        ),
        param(
            {
                "geometry": get_test_polygons(
                    "sites_multipolygon_with_hole", "API (uncleaned)"
                )
            },
            {"geometry": get_test_polygons("sites_multipolygon_with_hole", "QGIS")},
            id="sites multipolygon with hole",
        ),
    ]
    return test_variables, test_data


def get_test_polygons(polygon_name, source):
    path = f"./tests/data/clean_polygon_data/{source}/{polygon_name}.geojson"
    with open(path, "r") as f:
        return geojson.load(f)["features"]


shell1 = [(1, 0), (1, 1), (0, 1), (0, 0)]
shell2 = [(3, 2), (3, 3), (2, 3), (2, 2)]
hole = [(0.75, 0.25), (0.75, 0.75), (0.25, 0.75), (0.25, 0.25)]

polygon1 = Polygon(shell1)
polygon2 = Polygon(shell2)
polygon1_with_hole = Polygon(shell1, [hole])

simple_polygon1 = mapping(polygon1)
simple_polygon2 = mapping(polygon2)

polygon_with_hole = mapping(Polygon(shell2, [hole]))
multipolygon1 = mapping(MultiPolygon([polygon1, polygon2]))
multipolygon_with_hole = mapping(MultiPolygon([polygon2, polygon1_with_hole]))
