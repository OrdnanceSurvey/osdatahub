import os
import tempfile
import unittest.mock as mock
import dotenv

dotenv.load_dotenv()

import pytest
from osdatahub import OpenDataDownload, DataPackageDownload
from osdatahub.DownloadsAPI.downloads_api import _DownloadObj

from tests.data import downloads_data as data

API_KEY = os.environ.get("OSDATAHUB_TEST_KEY")


class TestOpenData:
    @pytest.fixture()
    def open_data_download(self):
        product = OpenDataDownload(product_id="test_id")
        yield product

    def test_product_init(self, open_data_download):
        assert open_data_download._ENDPOINT == "https://api.os.uk/downloads/v1/products"
        assert open_data_download.id == "test_id"

    @pytest.mark.parametrize(*data.product_list_pass("test_id"))
    @pytest.mark.usefixtures("open_data_download")
    @mock.patch('osdatahub.get')
    def test_product_list_pass(self, request_mocked, open_data_download, file_name, file_format, file_subformat, area,
                               return_downloadobj, expected_url, expected_params):
        open_data_download.product_list(file_name=file_name, file_format=file_format, file_subformat=file_subformat,
                                        area=area, return_downloadobj=return_downloadobj)
        request_mocked.assert_called_with(url=expected_url,
                                          params=expected_params,
                                          proxies={})

        assert type(return_downloadobj) == bool

    @pytest.mark.parametrize(*data.product_list_fail())
    def test_product_list_fail(self, open_data_download, file_name, file_format, file_subformat, area,
                               return_downloadobj, expected_result):
        with pytest.raises(expected_result):
            open_data_download.product_list(file_name=file_name, file_format=file_format,
                                            file_subformat=file_subformat,
                                            area=area, return_downloadobj=return_downloadobj)

    @pytest.mark.skipif(API_KEY is None, reason="Test API key not available")
    def test_product_list_live(self):
        greenspaces = OpenDataDownload("OpenGreenspace")
        greenspaces_info = greenspaces.product_list()
        assert type(greenspaces_info) is list
        assert type(greenspaces_info[0]) is dict

    # @pytest.mark.parametrize(*data.download_pass())
    # def test_download_pass(self, open_data_download, output_dir, download_multiple, overwrite, processes,
    #                        product_list_mock_return,
    #                        downloadobj_mock_return,
    #                        expected_download_return,
    #                        download_callded_value):
    #
    #     open_data_download.product_list = mock.Mock(return_value=product_list_mock_return)
    #     _DownloadObj.download = mock.Mock(return_value=downloadobj_mock_return)
    #     tqdm.tqdm = mock.Mock(return_value="tqdm")
    #     open_data_download = OpenDataDownload("OpenGreenspace")
    #     response = open_data_download.download(output_dir, download_multiple=download_multiple, overwrite=overwrite)
    #     assert response == expected_download_return
    #     _DownloadObj.download.assert_has_calls(download_called_value)

# TODO Fix Test for packages

# class TestDataPackage:
#     @pytest.fixture()
#     def data_package(self):
#         data_package = DataPackageDownload(key="test_key", product_id="test_id")
#         yield data_package

#     @pytest.mark.skipif(API_KEY is None, reason="Test API key not available")
#     def test_download_pass(self):
#         # Arrange
#         product_package = DataPackageDownload(API_KEY, "97")

#         # Act
#         with tempfile.TemporaryDirectory() as tmpdirname:
#             downloaded = product_package.download("17094", tmpdirname, "bld_fts_buildingpart_orderSummary.json")

#         # Assert
#         assert len(downloaded) == 1

#     def test_download_list_pass(self):
#         # TODO: implement download_list_pass
#         pass

#     def test_download_list_fail(self):
#         # TODO: implement download_list_fail
#         pass

#     def test_versions_pass(self):
#         # TODO: implement versions_pass
#         pass

#     def test_versions_fail(self):
#         # TODO: implement versions_fail
#         pass


# class TestDownloadObj:
#     @pytest.fixture()
#     def download_obj(self):
#         download_obj = _DownloadObj(url="test_url", file_name="test_file", size=256)
#         yield download_obj

#     def download_pass(self):
#         # TODO: implement _DownloadObj download pass
#         pass

#     def download_fail(self):
#         # TODO: implement _DownloadObje download fail
#         pass
