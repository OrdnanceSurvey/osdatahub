import requests
from typeguard import typechecked

from .download_executor import DownloadObj
from .downloads_api import DownloadsAPI
from osdatahub.codes import AREA_CODES


class Product(DownloadsAPI):
    _ENDPOINT = DownloadsAPI._ENDPOINT + "products"

    @typechecked
    def download_list(self, file_name: str = None, file_format: str = None, file_subformat: str = None,
                      area: str = None) -> list:
        """
        Returns a list of possible downloads for specific OS OpenData Product based on given filters
        """
        params = {}
        if area and area not in AREA_CODES:
            raise ValueError(f"Invalid argument \"area\". Had value {area} but must be one of {AREA_CODES}")

        if file_name:
            params.update({"fileName": file_name})
        if file_format:
            params.update({"format": file_format})
        if file_subformat:
            params.update({"subformat": file_subformat})
        if area:
            params.update({"area": area})

        response = requests.get(url=self._endpoint(f"{self.id}/downloads"), params=params)
        return [DownloadObj(url=download["url"], file_name=download["fileName"])
                for download in response.json()]

    def download(self, output_dir=".",
                 file_name: str = None,
                 file_format: str = None,
                 file_subformat: str = None,
                 area: str = None,
                 download_multiple=False,
                 overwrite=False,
                 processes=None):
        download_list = self.download_list(file_name=file_name, file_format=file_format, file_subformat=file_subformat,
                                           area=area)
        super().download(download_list=download_list,
                         output_dir=output_dir,
                         overwrite=overwrite,
                         download_multiple=download_multiple,
                         processes=processes)
