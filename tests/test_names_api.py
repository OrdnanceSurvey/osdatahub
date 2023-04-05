import unittest.mock as mock
from os import environ

import pytest
from osdatahub.NamesAPI.names_api import NamesAPI

from tests.data import names_data as data


class TestFind:
    @pytest.fixture()
    def names(self):
        names = NamesAPI("test")
        yield names

    @pytest.mark.parametrize(*data.test_find_pass())
    @pytest.mark.usefixtures("names")
    @mock.patch('osdatahub.get')
    def test_find_pass(self, request_mocked, names, text, limit, bounds, bbox_filter, local_type,
                       expected_url, expected_params):
        names.find(text, limit=limit, bounds=bounds, bbox_filter=bbox_filter, local_type=local_type)
        request_mocked.assert_called_with(expected_url,
                                          params=expected_params,
                                          proxies={})

    @pytest.mark.parametrize(*data.test_find_fail())
    @pytest.mark.usefixtures("names")
    def test_find_fail(self, names, text, limit, bounds, bbox_filter, local_type, expected_result):
        with pytest.raises(expected_exception=expected_result):
            names.find(text, limit=limit, bounds=bounds, bbox_filter=bbox_filter, local_type=local_type)


class TestNearest:
    @pytest.fixture()
    def names(self):
        names = NamesAPI("test")
        yield names

    @pytest.mark.parametrize(*data.test_nearest_pass())
    @pytest.mark.usefixtures("names")
    @mock.patch('osdatahub.get')
    def test_nearest_pass(self, request_mocked, names, point, radius, local_type, expected_url, expected_params):
        names.nearest(point=point, radius=radius, local_type=local_type)
        request_mocked.assert_called_with(expected_url,
                                          params=expected_params,
                                          proxies={})

    @pytest.mark.parametrize(*data.test_nearest_fail())
    @pytest.mark.usefixtures("names")
    def test_nearest_fail(self, names, point, radius, local_type, expected_result):
        with pytest.raises(expected_exception=expected_result):
            names.nearest(point=point, radius=radius, local_type=local_type)


class TestFormatFq:
    @pytest.fixture()
    def names(self):
        key = environ.get("OS_API_KEY")
        names = NamesAPI(key)
        yield names

    @pytest.mark.parametrize(*data.test_format_fq())
    @pytest.mark.usefixtures("names")
    def test_format_fq_pass(self, names, bbox, local_type, expected_result):
        fq_args = names._NamesAPI__format_fq(bbox_filter=bbox, local_type=local_type)
        assert fq_args == expected_result

    @pytest.mark.parametrize(*data.test_format_fq_errors())
    @pytest.mark.usefixtures("names")
    def test_format_fq_errors(self, names, bbox, local_type, expected_result):
        # Act
        with pytest.raises(expected_result):
            fq_args = names._NamesAPI__format_fq(bbox_filter=bbox, local_type=local_type)
