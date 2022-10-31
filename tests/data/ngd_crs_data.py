from osdatahub.NGDAPI.crs import EPSG
from pytest import param


def test_ngd_crs():
    test_variables = "crs, epsg, valid_crs, expected_result"
    test_data = [
        param("epsg:4326", None, EPSG, EPSG["epsg:4326"]),
        param("EpSg:4326", None, EPSG, EPSG["epsg:4326"]),
        param("EPSG:27700",  None, EPSG, EPSG["epsg:27700"]),
        param("EPSG:7405",  None, EPSG, EPSG["epsg:7405"]),
        param("EPSG:3857",  None, EPSG, EPSG["epsg:3857"]),
        param("crs84",  None, EPSG, EPSG["crs84"]),
        param("CRS84",  None, EPSG, EPSG["crs84"]),
        param(None, 4326,EPSG, EPSG["epsg:4326"]),
        param(None,3857, EPSG,EPSG["epsg:3857"]),
        param(None,27700,EPSG, EPSG["epsg:27700"]),
        param(None,7405,EPSG, EPSG["epsg:7405"]),
    ]
    return test_variables, test_data


def test_ngd_crs_fail():
    test_variables = "crs, expected_result"
    test_data = [
        param("TEST", ValueError)
    ]
    return test_variables, test_data


def test_merge_geojsons_pass():
    test_variables = "crs, expected_result"
    test_data = [
        param("TEST", ValueError)
    ]
    return test_variables, test_data