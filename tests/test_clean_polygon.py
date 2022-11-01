import pytest
from osdatahub.utils import clean_polygon

from tests.data import clean_polygon_data as data


class TestCleanPolygon:
    @pytest.mark.parametrize(*data.test_clean_polygon())
    def test_clean_polygon(self, feature, expected_result):
        # Act
        geojson = clean_polygon(feature)

        # Assert
        assert geojson == expected_result
