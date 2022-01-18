import pytest

from osdatahub.DownloadsAPI import Product, DataPackage
from osdatahub.DownloadsAPI.downloads_api import _DownloadsAPIBase, _DownloadObj


class TestProduct:
    @pytest.fixture()
    def product(self):
        product = Product(key="test_key", product_id="test_id")
        yield product

    def test_download_list_pass(self):
        # TODO: implement product download_list_pass
        pass

    def test_download_list_fail(self):
        # TODO: implement product download_list_fail
        pass


class TestDataPackage:
    @pytest.fixture()
    def data_package(self):
        data_package = DataPackage(key="test_key", product_id="test_id")
        yield data_package

    def test_download_list_pass(self):
        # TODO: implement download_list_pass
        pass

    def test_download_list_fail(self):
        # TODO: implement download_list_fail
        pass

    def test_versions_pass(self):
        # TODO: implement versions_pass
        pass

    def test_versions_fail(self):
        # TODO: implement versions_fail
        pass


class TestDownloadsAPIBase:
    @pytest.fixture()
    def downloads_api_base(self):
        # TODO: check this fixture works
        downloads_api_base = _DownloadsAPIBase(key="test_key", product_id="test_id")
        yield downloads_api_base

    def test_details(self):
        # TODO: implement base details
        pass

    def test_all_products(self):
        # TODO: implement base all_products
        pass

    def test_downloads_pass(self):
        # TODO: implement base _download pass
        pass

    def test_downloads_fail(self):
        # TODO: implement base _download fail
        pass


class TestDownloadObj:
    @pytest.fixture()
    def download_obj(self):
        download_obj = _DownloadObj(url="test_url", file_name="test_file")
        yield download_obj

    def download_pass(self):
        # TODO: implement _DownloadObj download pass
        pass

    def download_fail(self):
        # TODO: implement _DownloadObje download fail
        pass