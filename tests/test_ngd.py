from os import environ
import geopandas
import requests
import json
from shapely.geometry import Polygon
from osdatahub import Extent
from osdatahub import NGDAPI
from datetime import datetime

import pytest

from osdatahub.NGDAPI.crs import get_crs
from osdatahub.NGDAPI.ngd_api import merge_geojsons

from tests.data import ngd_crs_data as crs_data
from tests.data import ngd_merge_geojsons_data as merge_geojsons_data


class TestNGDCRS:
    @pytest.mark.parametrize(*crs_data.test_ngd_crs())
    def test_ngd_crs_pass(self, crs, epsg, valid_crs, expected_result):
        assert get_crs(crs, epsg, valid_crs) == expected_result

    @pytest.mark.parametrize(*crs_data.test_ngd_crs_fail())
    def test_ngd_crs_fail(self, crs, expected_result):
        with pytest.raises(expected_exception=expected_result):
            get_crs(crs)


class TestNGD:
    def test_ngd_api_call(self, extent, crs, start_datetime, end_datetime, filter, filter_crs, limit, offset, epsg, expected_result):
        pass


class TestMergeGeojsons:
    @pytest.mark.parametrize(*merge_geojsons_data.test_merge_geojsons_pass())
    def test_merge_geojsons_pass(self, gj1, gj2, expected_number):
        m = merge_geojsons(gj1, gj2)
        assert m["numberReturned"] == expected_number
        assert len(m["features"]) == expected_number
        assert


    @pytest.mark.parametrize(*merge_geojsons_data.test_merge_geojsons_fail())
    def test_merge_geojsons_fail(self, gj1, gj2, expected_result):
        with pytest.raises(expected_exception=expected_result):
            merge_geojsons(gj1, gj2)
