import unittest.mock as mock

import pytest
from osdatahub import FeaturesAPI

from tests.data import features_api_data as data


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

    @pytest.mark.parametrize(*data.test_query_pass())
    @mock.patch('requests.get')
    def test_query_pass(self, request_mocked, extent, product, filters,
                        limit, expected_url, expected_params):
        features_api = FeaturesAPI("API-KEY", product, extent)
        for filter in filters:
            features_api.add_filters(filter)

        features_api.query(limit=limit)
        request_mocked.assert_called_with(expected_url,
                                          params=expected_params)
