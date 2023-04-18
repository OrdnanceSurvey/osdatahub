from unittest import mock
from os import environ
from dotenv import load_dotenv

import pytest
from osdatahub.NGD.crs import get_crs
from osdatahub.NGD.ngd_api import _merge_geojsons, NGD

from tests.data import ngd_crs_data as crs_data
from tests.data import ngd_merge_geojsons_data as merge_geojsons_data
from tests.data import ngd_query_data as query_data

load_dotenv()

API_KEY = environ.get("OSDATAHUB_TEST_KEY")


class TestNGDCRS:
    @pytest.mark.parametrize(*crs_data.test_ngd_crs())
    def test_ngd_crs_pass(self, crs, valid_crs, expected_result):
        assert get_crs(crs, valid_crs) == expected_result

    @pytest.mark.parametrize(*crs_data.test_ngd_crs_fail())
    def test_ngd_crs_fail(self, crs, valid_crs, expected_result):
        with pytest.raises(expected_exception=expected_result):
            get_crs(crs, valid_crs)


class TestNGDQuery:
    @pytest.mark.parametrize(*query_data.test_ngd_instantiation())
    @mock.patch('osdatahub.get')
    def test_ngd_instantiation(self, request_mocked, api_key, collection, expected_url, expected_headers):
        request_mocked.return_value.configure_mock(json=lambda: {"features": [], "numberReturned": 0})

        ngd = NGD(key=api_key, collection=collection)
        ngd.query()

        request_mocked.assert_called_with(expected_url,
                                          headers=expected_headers,
                                          params={"limit": 100, "offset": 0},
                                          proxies={})

    @pytest.mark.parametrize(*query_data.test_ngd_query())
    @mock.patch('osdatahub.get')
    def test_ngd_api_call(self, request_mocked, extent, crs, start_datetime, end_datetime, cql_filter, filter_crs,
                          max_results, offset, expected_url, expected_params):
        request_mocked.return_value.configure_mock(json=lambda: {"features": [], "numberReturned": 0})

        ngd = NGD(key="API-KEY", collection="bld-fts-buildingline")

        ngd.query(extent=extent,
                  crs=crs,
                  start_datetime=start_datetime,
                  end_datetime=end_datetime,
                  cql_filter=cql_filter,
                  filter_crs=filter_crs,
                  max_results=max_results,
                  offset=offset
                  )
        request_mocked.assert_called_with(expected_url,
                                          params=expected_params,
                                          headers={"key": "API-KEY"},
                                          proxies={})

    @pytest.mark.parametrize(*query_data.test_ngd_query_fail())
    def test_ngd_api_call_fail(self, extent, crs, start_datetime, end_datetime, cql_filter, filter_crs,
                               max_results, offset, expected_error):
        ngd = NGD("API_KEY", "blt-fts-buildingline")
        with pytest.raises(expected_exception=expected_error):
            ngd.query(extent=extent,
                      crs=crs,
                      start_datetime=start_datetime,
                      end_datetime=end_datetime,
                      cql_filter=cql_filter,
                      filter_crs=filter_crs,
                      max_results=max_results,
                      offset=offset
                      )

    @pytest.mark.skipif(not API_KEY, reason="Test API key not available")
    @pytest.mark.parametrize(*query_data.test_ngd_query_live())
    def test_ngd_api_call(self, collection, extent, crs, start_datetime, end_datetime, cql_filter, filter_crs,
                          max_results, offset):
        ngd = NGD(key=API_KEY, collection=collection)
        results = ngd.query(extent=extent,
                  crs=crs,
                  start_datetime=start_datetime,
                  end_datetime=end_datetime,
                  cql_filter=cql_filter,
                  filter_crs=filter_crs,
                  max_results=max_results,
                  offset=offset
                )

        assert len(results["features"]) == max_results


class TestNGDGetCollections:
    @mock.patch('osdatahub.get')
    def test_ngd_get_collections(self, request_mocked):
        request_mocked.return_value.configure_mock(json=lambda: {})
        NGD.get_collections()

        request_mocked.assert_called_with("https://api.os.uk/features/ngd/ofa/v1/collections",
                                          proxies={})


class TestNGDQueryFeature:

    @pytest.mark.parametrize(*query_data.test_ngd_query_feature())
    @mock.patch('osdatahub.get')
    def test_ngd_query_filter(self, request_mocked, feature_id, crs, expected_url, expected_params):
        request_mocked.return_value.configure_mock(json=lambda: {})
        ngd = NGD("api_key", "bld-fts-buildingline")
        ngd.query_feature(feature_id=feature_id, crs=crs)

        request_mocked.assert_called_with(expected_url,
                                          params=expected_params,
                                          headers={"key": "api_key"},
                                          proxies={})


class TestMergeGeojsons:
    @pytest.mark.parametrize(*merge_geojsons_data.test_merge_geojsons_pass())
    def test_merge_geojsons_pass(self, gj1, gj2, expected_result):
        m = _merge_geojsons(gj1, gj2)
        assert m["numberReturned"] == expected_result
        assert len(m["features"]) == expected_result

    @pytest.mark.parametrize(*merge_geojsons_data.test_merge_geojsons_fail())
    def test_merge_geojsons_fail(self, gj1, gj2, expected_result):
        with pytest.raises(expected_exception=expected_result):
            _merge_geojsons(gj1, gj2)
