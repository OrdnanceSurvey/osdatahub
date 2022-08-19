import operator

from osdatahub import Extent
from osdatahub.filters import is_equal, is_less_than, filter_and, filter_or
from pytest import param


def test_get_single_attribute_filter():
    test_variables = "property_name, filter_type, a, expected_result"
    test_data = [
        param(
            "Theme",
            "PropertyIsEqualTo",
            "Building",
            "<ogc:PropertyIsEqualTo><ogc:PropertyName>Theme</ogc:PropertyName><ogc:Literal>Building</ogc:Literal></ogc:PropertyIsEqualTo>",
            id="equal to string",
        ),
        param(
            "Theme",
            "PropertyIsEqualTo",
            "Road",
            "<ogc:PropertyIsEqualTo><ogc:PropertyName>Theme</ogc:PropertyName><ogc:Literal>Road</ogc:Literal></ogc:PropertyIsEqualTo>",
            id="equal to string",
        ),
    ]
    return test_variables, test_data


def test_between():
    test_variables = "property_name, lower, upper, expected_result"
    test_data = [
        param(
            "Width",
            5,
            10,
            f"<ogc:PropertyIsBetween><ogc:PropertyName>Width</ogc:PropertyName><LowerBoundary><ogc:Literal>5</ogc:Literal></LowerBoundary><UpperBoundary><ogc:Literal>10</ogc:Literal></UpperBoundary></ogc:PropertyIsBetween>",
            id="between two ints",
        ),
    ]
    return test_variables, test_data


def test_intersects():
    test_variables = "extent, expected_result"
    test_data = [
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:27700"),
            "<ogc:Intersects>"
            "<ogc:PropertyName>SHAPE</ogc:PropertyName>"
            "<gml:Polygon xmlns:gml='http://www.opengis.net/gml' srsName='EPSG:27700'>"
            "<gml:outerBoundaryIs>"
            "<gml:LinearRing>"
            '<gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates>'
            "</gml:LinearRing>"
            "</gml:outerBoundaryIs>"
            "</gml:Polygon>"
            "</ogc:Intersects>",
            id="EPSG:27700 - bbox",
        ),
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:3857"),
            "<ogc:Intersects>"
            "<ogc:PropertyName>SHAPE</ogc:PropertyName>"
            "<gml:Polygon xmlns:gml='http://www.opengis.net/gml' srsName='EPSG:3857'>"
            "<gml:outerBoundaryIs>"
            "<gml:LinearRing>"
            '<gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates>'
            "</gml:LinearRing>"
            "</gml:outerBoundaryIs>"
            "</gml:Polygon>"
            "</ogc:Intersects>",
            id="EPSG:3857 - bbox",
        ),
        param(
            Extent.from_bbox((0, 0, 1, 1), "epsg:3857"),
            "<ogc:Intersects>"
            "<ogc:PropertyName>SHAPE</ogc:PropertyName>"
            "<gml:Polygon xmlns:gml='http://www.opengis.net/gml' srsName='EPSG:3857'>"
            "<gml:outerBoundaryIs>"
            "<gml:LinearRing>"
            '<gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates>'
            "</gml:LinearRing>"
            "</gml:outerBoundaryIs>"
            "</gml:Polygon>"
            "</ogc:Intersects>",
            id="epsg:3857 - bbox",
        ),
    ]
    return test_variables, test_data


def test_logical():
    test_variables = "filter1, filter2, filter3, op1, op2, op3, expected_result"
    filter_eq = is_equal("eq_property", "eq_value")
    filter_lt = is_less_than("lt_property", 0)
    filter_gt = is_less_than("lt_property", 0)
    test_data = [
        param(
            filter_eq,
            filter_lt,
            filter_gt,
            operator.and_,
            filter_and,
            operator.or_,
            f"<ogc:Or><ogc:And>{filter_eq}{filter_lt}</ogc:And><ogc:And>{filter_lt}{filter_gt}</ogc:And></ogc:Or>",
            id="operator equals string",
        ),
        param(
            filter_eq,
            filter_lt,
            filter_gt,
            operator.or_,
            operator.and_,
            filter_or,
            f"<ogc:Or><ogc:Or>{filter_eq}{filter_lt}</ogc:Or><ogc:And>{filter_lt}{filter_gt}</ogc:And></ogc:Or>",
            id="operator equals string",
        ),
    ]
    return test_variables, test_data
