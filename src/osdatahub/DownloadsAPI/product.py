import logging
import os
from dataclasses import dataclass
from typing import Optional

import requests
from typeguard import typechecked

from .download_executor import Download
from .downloads_api import DownloadsAPI
from osdatahub.codes import AREA_CODES


class Product(DownloadsAPI):
    _ENDPOINT = DownloadsAPI._ENDPOINT + "products"

    @typechecked
    def downloads_list(self, file_name: str = None, format: str = None, subformat: str = None, area: str = None):
        """
        Returns a list of possible downloads for specific OS OpenData Product based on given filters
        """
        params = {}
        if area and area not in AREA_CODES:
            raise ValueError(f"Invalid argument \"area\". Had value {area} but must be one of {AREA_CODES}")

        if file_name:
            params.update({"fileName": file_name})
        if format:
            params.update({"format": format})
        if subformat:
            params.update({"subformat": subformat})
        if area:
            params.update({"area": area})

        response = requests.get(url=self._endpoint(f"{self.id}/downloads"), params=params)
        return [Download(url=download["url"], file_name=download["fileName"], file_format=download["format"])
                for download in response.json()]

    @typechecked
    def download(self, file_name: str = None, format: str = None, subformat: str = None, area: str = None):
        downloads = self.downloads_list(
            file_name=file_name,
            format=format,
            subformat=subformat,
            area=area
        )



