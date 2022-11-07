from osdatahub.NGD.crs import EPSG
from pytest import param


def test_ngd_crs():
    test_variables = "crs, valid_crs, expected_result"
    test_data = [
        param("epsg:4326", EPSG, EPSG["epsg:4326"]),
        param("EpSg:4326", EPSG, EPSG["epsg:4326"]),
        param("EPSG:27700", EPSG, EPSG["epsg:27700"]),
        param("EPSG:7405", EPSG, EPSG["epsg:7405"]),
        param("EPSG:3857", EPSG, EPSG["epsg:3857"]),
        param("crs84", EPSG, EPSG["crs84"]),
        param("CRS84", EPSG, EPSG["crs84"]),
        param(4326, EPSG, EPSG["epsg:4326"]),
        param(3857, EPSG, EPSG["epsg:3857"]),
        param(27700, EPSG, EPSG["epsg:27700"]),
        param(7405, EPSG, EPSG["epsg:7405"]),
        param(7405, ["epsg:7405"], EPSG["epsg:7405"]),
        param(3857, ("epsg:7405", "epsg:3857"), EPSG["epsg:3857"]),
        param("http://www.opengis.net/def/crs/EPSG/0/4326/", EPSG, EPSG["epsg:4326"]),
        param("www.opengis.net/def/crs/EPSG/0/4326", EPSG, EPSG["epsg:4326"]),
        param("http://www.opengis.net/def/crs/OGC/1.3/crs84", EPSG, EPSG["crs84"]),
        param("HTTPS://www.opengis.net/def/crs/OGC/1.3/CRS84", EPSG, EPSG["crs84"]),
    ]
    return test_variables, test_data


def test_ngd_crs_fail():
    test_variables = "crs, valid_crs, expected_result"
    test_data = [
        param("TEST", EPSG, ValueError),
        param(4326, ("EPSG:7405", "EPSG:3857"), ValueError)
    ]
    return test_variables, test_data


def test_merge_geojsons_pass():
    test_variables = "crs, expected_result"
    test_data = [
        param("TEST", ValueError)
    ]
    return test_variables, test_data
