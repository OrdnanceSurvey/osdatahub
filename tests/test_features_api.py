import pytest

from osdatahub import FeaturesAPI
from tests.data import features_api_data as data


class TestFeaturesAPI:
    @pytest.mark.parametrize(*data.test__params())
    def test__params(self, extent, product, expected_result, filters):
        # Arrange
        features_api = FeaturesAPI("API-KEY", product, extent)
        for filter in filters:
            features_api.add_filters(filter)

        # Act
        params = features_api._FeaturesAPI__params
        print(params)

        # Assert
        assert params == expected_result
