import pytest
from os import environ
import unittest.mock as mock

from osdatahub.MatchAndCleanseAPI.match_and_cleanse_api import MatchAndCleanseAPI
from tests.data import test_match_and_cleanse_api_data as data


class TestMatch:
    @pytest.fixture()
    def match_and_cleanse(self):
        match_and_cleanse = MatchAndCleanseAPI("test")
        yield match_and_cleanse

    @pytest.mark.parametrize(*data.test_match_pass())
    @pytest.mark.usefixtures("match_and_cleanse")
    @mock.patch('requests.get')
    def test_match_pass(self, request_mocked, match_and_cleanse, text, limit, output_crs, dataset, min_match,
                        match_precision, classification_code, logical_status_code, country_code, expected_url,
                        expected_params):
        match_and_cleanse.match(text, limit, output_crs, dataset, min_match, match_precision, classification_code,
                                logical_status_code, country_code)
        request_mocked.assert_called_with(expected_url,
                                          params=expected_params)

    @pytest.mark.parametrize(*data.test_match_fail())
    @pytest.mark.usefixtures("match_and_cleanse")
    def test_match_fail(self, match_and_cleanse, text, limit, output_crs, dataset, min_match,
                        match_precision, classification_code, logical_status_code, country_code, expected_error):
        with pytest.raises(expected_exception=expected_error):
            match_and_cleanse.match(text, limit, output_crs, dataset, min_match, match_precision, classification_code,
                                    logical_status_code, country_code)