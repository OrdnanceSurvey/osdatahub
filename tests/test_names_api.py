import pytest
from os import environ

from osdatahub.NamesAPI.names_api import NamesAPI
from tests.data import names_data as data


class TestFind:
    pass


class TestNearest:
    pass


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
