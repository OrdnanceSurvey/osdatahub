import pytest
from osdatahub.filters import is_between, single_attribute_filter, intersects

from tests.data import filters_data as data


class TestFiltering:
    @pytest.mark.parametrize(*data.test_get_single_attribute_filter())
    def test_get_single_attribute_filter(
            self, property_name, filter_type, a, expected_result
    ):
        # Act
        extent_filter = single_attribute_filter(property_name, filter_type, a)

        # Assert
        assert extent_filter == expected_result

    @pytest.mark.parametrize(*data.test_between())
    def test_between(self, property_name, lower, upper, expected_result):
        # Act
        extent_filter = is_between(property_name, lower, upper)

        # Assert
        assert extent_filter == expected_result

    @pytest.mark.parametrize(*data.test_intersects())
    def test_intersects(self, extent, expected_result):
        # Act
        extent_filter = intersects(extent)

        # Assert
        assert extent_filter == expected_result

    @pytest.mark.parametrize(*data.test_logical())
    def test_logical(self, filter1, filter2, filter3, op1, op2, op3, expected_result):
        # Act
        result = op3(op1(filter1, filter2), op2(filter2, filter3))

        # Assert
        assert result == expected_result
