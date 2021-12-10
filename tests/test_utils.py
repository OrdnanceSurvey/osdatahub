import pytest

from osdatahub.utils import address_to_feature
from tests.data import utils_data as data


class TestAddressToFeature:
    @pytest.mark.parametrize(*data.test_convert_address_to_feature())
    def test_convert_address_to_feature(self, address, crs, expected_result):
        # Act
        address_feature = address_to_feature(address, crs)
        # Assert
        assert address_feature == expected_result

    @pytest.mark.parametrize(*data.test_address_to_feature_error())
    def test_address_to_feature_error(self, address, crs):
        # Act
        with pytest.raises(ValueError):
            address_feature = address_to_feature(address, crs)
