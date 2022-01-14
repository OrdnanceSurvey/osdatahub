import functools

import requests

from .downloads_api import DownloadsAPI


class DataPackage(DownloadsAPI):
    _ENDPOINT = DownloadsAPI._ENDPOINT + "dataPackages"

    @functools.cached_property
    def versions(self):
        return requests.get(self._endpoint(f"{self.id}/versions")).json()

    def downl
