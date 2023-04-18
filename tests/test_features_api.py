import os
import unittest.mock as mock

import pytest
from osdatahub import FeaturesAPI

from tests.data import features_api_data as data

API_KEY = os.environ.get("OSDATAHUB_TEST_KEY")


class TestFeaturesAPI:
    @pytest.mark.parametrize(*data.test__params())
    def test__params(self, extent, product, filters, expected_result):
        # Arrange
        features_api = FeaturesAPI("API-KEY", product, extent)
        for filter in filters:
            features_api.add_filters(filter)

        # Act
        params = features_api._FeaturesAPI__params

        # Assert
        assert params == expected_result

    @pytest.mark.parametrize(*data.test_request_params())
    @mock.patch('osdatahub.get')
    def test_request_params(self, request_mocked, extent, product, filters,
                            limit, expected_url, expected_params):
        # Arrange
        request_mocked.return_value.configure_mock(json=lambda: {"features": []})
        features_api = FeaturesAPI("API-KEY", product, extent)
        for filter in filters:
            features_api.add_filters(filter)

        # Act
        features_api.query(limit=limit)

        # Assert
        request_mocked.assert_called_with(expected_url,
                                          params=expected_params,
                                          proxies={})

    @pytest.mark.skipif(not API_KEY, reason="Test API key not available")
    @pytest.mark.parametrize(*data.test_query())
    def test_query(self, product, extent, limit, expected_count):
        # Arrange
        features_api = FeaturesAPI(API_KEY, product, extent)

        # Act
        results = features_api.query(limit=limit)

        # Assert
        assert len(results["features"]) == expected_count
