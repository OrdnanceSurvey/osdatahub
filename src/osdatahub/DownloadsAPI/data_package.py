import functools
import requests
from typeguard import typechecked

from .download_executor import DownloadObj
from .downloads_api import DownloadsAPI


class DataPackage(DownloadsAPI):
    _ENDPOINT = DownloadsAPI._ENDPOINT + "dataPackages"

    @functools.cached_property
    def versions(self):
        return requests.get(self._endpoint(f"{self.id}/versions")).json()

    @typechecked
    def download_list(self, version_id: str, file_name=None):
        endpoint = self._endpoint(f"{self.id}/versions/{version_id}")
        params = {}
        if file_name:
            endpoint += "/downloads"
            params.update({"fileName": file_name})
        response = requests.get(url=endpoint, params=params)
        return [DownloadObj(url=download["url"], file_name=download["fileName"])
                for download in response.json()["downloads"]]

    def download(self,
                 version_id: str,
                 output_dir=".",
                 file_name: str = None,
                 download_multiple=False,
                 overwrite=False,
                 processes=None):
        download_list = self.download_list(version_id)
        super().download(download_list=download_list,
                         output_dir=output_dir,
                         overwrite=overwrite,
                         download_multiple=download_multiple,
                         processes=processes)
