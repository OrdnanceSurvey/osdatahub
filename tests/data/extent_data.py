import json

from osdatahub import Extent
from osdatahub.bbox import BBox
from pytest import param
from shapely.geometry import box, Polygon, Point


def test_from_bbox():
    test_variables = "bbox, crs, expected_result"
    test_data = [
        param(
            (600000, 310200, 600900, 310800),
            "epsg:27700",
            Extent(box(600000, 310200, 600900, 310800), "epsg:27700"),
            id="tuple bbox",
        ),
        param(
            BBox(600000, 310200, 600900, 310800),
            "epsg:27700",
            Extent(box(600000, 310200, 600900, 310800), "epsg:27700"),
            id="bbox object",
        ),
    ]
    return test_variables, test_data


def test_from_radius():
    test_variables = "centre, radius, crs, expected_result, expected_bbox"
    test_data = [
        param(
            (0, 0),
            10,
            "epsg:27700",
            Extent(Point(0, 0).buffer(10), "epsg:27700"),
            BBox(-10, -10, 10, 10),
            id="tuple centre",
        ),
        param(
            Point(0, 0),
            10,
            "epsg:27700",
            Extent(Point(0, 0).buffer(10), "epsg:27700"),
            BBox(-10, -10, 10, 10),
            id="shapely point centre",
        ),
        param(
            [0, 0],
            10,
            "epsg:27700",
            Extent(Point(0, 0).buffer(10), "epsg:27700"),
            BBox(-10, -10, 10, 10),
            id="list centre",
        ),
    ]
    return test_variables, test_data


def test_set_crs():
    test_variables = "initital_polygon, initital_crs, updated_crs, expected_result"
    test_data = [
        param(
            Polygon(),
            "epsg:27700",
            "epsg:3857",
            Extent(Polygon(), "epsg:3857"),
            id="set crs",
        )
    ]
    return test_variables, test_data


def test_is_within():
    test_variables = "polygon, crs, bounds, expected_result"
    test_data = [
        param(
            Polygon([(0, 0), (5, 5), (10, 0)]),
            "epsg:27700",
            (0, 0, 10, 5),
            True,
            id="tuple bbox - is equal to bounds",
        ),
        param(
            Polygon([(0, 0), (5, 5), (10, 0)]),
            "epsg:27700",
            (0, 0, 1, 5),
            False,
            id="tuple bbox - is not within",
        ),
        param(
            Polygon([(0, 0), (5, 5), (10, 0)]),
            "epsg:27700",
            (-1, -1, 15, 15),
            True,
            id="tuple bbox - is fully within",
        ),
        param(
            Polygon([(0, 0), (5, 5), (10, 0)]),
            "epsg:27700",
            BBox(-1, -1, 15, 15),
            True,
            id="BBox object - is fully within",
        ),
    ]
    return test_variables, test_data


def test_xml_coords():
    test_variables = "polygon, crs, expected_result"
    test_data = [
        param(
            Polygon([(0, 0), (5, 5), (10, 0)]),
            "epsg:27700",
            "0.0,0.0 5.0,5.0 10.0,0.0 0.0,0.0",
            id="triangle",
        ),
        param(
            Polygon([(0, 0), (5, 7), (10, 0)]),
            "epsg:27700",
            "0.0,0.0 5.0,7.0 10.0,0.0 0.0,0.0",
            id="triangle",
        ),
        param(
            Polygon([(-3.29, 50.74), (-3.27, 50.74), (-3.27, 50.76)]),
            "epsg:4326",
            "50.74,-3.29 50.74,-3.27 50.76,-3.27 50.74,-3.29",
            id="bbox object - lonlat input",
        ),
    ]
    return test_variables, test_data


def test_from_ons_code():
    test_variables = "ons_code, ons_mock_response, expected_result"
    test_data = [
        param(
            "E0100001",
            json.dumps(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [[[0, 0], [1, 1], [2, 0]]],
                            },
                        }
                    ],
                }
            ),
            Extent(Polygon([(0, 0), (1, 1), (2, 0)]), "EPSG:4326"),
            id="triangle",
        )
    ]
    return test_variables, test_data


def test_from_ons_code_error():
    test_variables = "ons_code, ons_mock_response"
    test_data = [
        param(
            "E0100001",
            json.dumps(
                {
                    "type": "FeatureCollection",
                    "features": [
                        {
                            "type": "Feature",
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [[[0, 0], [1, 1], [2, 0]]],
                            },
                        }
                    ],
                }
            ),
            id="line",
        )
    ]
    return test_variables, test_data


def test_to_json():
    test_variables = "polygon, crs, expected_result"
    test_data = [
        param(
            Polygon([(0, 0), (5, 5), (10, 0)]),
            "epsg:27700",
            {"type": "Polygon", "coordinates": [[(0, 0), (5, 5), (10, 0), (0, 0)]]},
            id="triangle - BNG",
        ),
        param(
            Polygon([(-3.29, 50.74), (-3.27, 50.74), (-3.27, 50.76)]),
            "epsg:4326",
            {
                "type": "Polygon",
                "coordinates": [
                    [(50.74, -3.29), (50.74, -3.27), (50.76, -3.27), (50.74, -3.29)]
                ],
            },
            id="triangle - lonlat",
        ),
    ]
    return test_variables, test_data
