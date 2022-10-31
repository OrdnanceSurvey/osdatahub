import pytest
import requests_mock
from osdatahub import Extent

from tests.data import extent_data as data


class TestExtent:
    @pytest.mark.parametrize(*data.test_from_bbox())
    def test_from_bbox(self, bbox, crs, expected_result):
        # Act
        extent = Extent.from_bbox(bbox, crs)

        # Assert
        assert extent == expected_result

    @pytest.mark.parametrize(*data.test_from_radius())
    def test_from_radius(self, centre, radius, crs, expected_result, expected_bbox):
        # Act
        extent = Extent.from_radius(centre, radius, crs)

        # Assert
        assert extent == expected_result
        assert extent.bbox == expected_bbox

    @pytest.mark.parametrize(*data.test_set_crs())
    def test_set_crs(
            self, initital_polygon, initital_crs, updated_crs, expected_result
    ):
        # Arrange
        extent = Extent(initital_polygon, initital_crs)

        # Act
        extent = extent.set_crs(updated_crs)

        # Assert
        assert extent == expected_result

    @pytest.mark.parametrize(*data.test_is_within())
    def test_is_within(self, polygon, crs, bounds, expected_result):
        # Arrange
        extent = Extent(polygon, crs)

        # Act
        within = extent.is_within(bounds)

        # Assert
        assert within == expected_result

    @pytest.mark.parametrize(*data.test_xml_coords())
    def test_xml_coords(self, polygon, crs, expected_result):
        # Arrange
        extent = Extent(polygon, crs)

        # Act
        xml_coords = extent.xml_coords

        # Assert
        assert xml_coords == expected_result

    @pytest.mark.parametrize(*data.test_to_json())
    def test_to_json(self, polygon, crs, expected_result):
        # Arrange
        extent = Extent(polygon, crs)

        # Act
        json = extent.to_json()
        print(json)
        print(expected_result)

        # Assert
        assert json == expected_result


@pytest.mark.parametrize(*data.test_from_ons_code())
def test_from_ons_code(ons_code, ons_mock_response, expected_result):
    # Arrange
    from osdatahub.ons_api import ID_ENDPOINT

    endpoint = f"{ID_ENDPOINT}{ons_code}"

    # Act
    with requests_mock.Mocker() as m:
        m.register_uri("GET", endpoint, text=ons_mock_response)
        extent = Extent.from_ons_code(ons_code)

        # Assert
        assert extent == expected_result


@pytest.mark.parametrize(*data.test_from_ons_code_error())
def test_from_ons_code_error(ons_code, ons_mock_response):
    # Arrange
    from osdatahub.ons_api import ID_ENDPOINT

    endpoint = f"{ID_ENDPOINT}{ons_code}"

    # Act
    with requests_mock.Mocker() as m:
        m.register_uri("GET", endpoint, text=ons_mock_response)
        with pytest.raises(ValueError):
            Extent.from_ons_code(ons_code)
