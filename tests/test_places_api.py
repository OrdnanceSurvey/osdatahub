from os import environ

import pytest
from osdatahub.PlacesAPI.places_api import PlacesAPI

from tests.data import places_data as data


class TestFormatFq:
    @pytest.fixture()
    def places(self):
        key = environ.get("OS_API_KEY")
        places = PlacesAPI(key)
        yield places

    @pytest.mark.parametrize(*data.test_format_fq())
    @pytest.mark.usefixtures("places")
    def test_format_fq_pass(
            self, places, classification_codes, logical_states, expected_result
    ):
        # Act
        fq_args = places._PlacesAPI__format_fq(
            classification_code=classification_codes, logical_status_code=logical_states
        )
        # Assert
        assert fq_args == expected_result

    @pytest.mark.parametrize(*data.test_format_fq_errors())
    @pytest.mark.usefixtures("places")
    def test_format_fq_errors(
            self, places, classification_codes, logical_states, expected_result
    ):
        # Act
        with pytest.raises(expected_result):
            fq_args = places._PlacesAPI__format_fq(
                classification_code=classification_codes,
                logical_status_code=logical_states,
            )
