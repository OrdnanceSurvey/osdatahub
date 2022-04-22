import functools
from pathlib import Path
from typing import Union

import requests
from typeguard import typechecked

from .downloads_api import _DownloadsAPIBase, _DownloadObj


class DataPackageDownload(_DownloadsAPIBase):
    """
    Main class for downloading OS Premium Data Packages
    (https://osdatahub.os.uk/docs/downloads/technicalSpecification#/Data%20Packages)

    Args:
        key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/
        product_id (str): Valid ID for Downloads API  DataPackage.

    """
    _ENDPOINT = _DownloadsAPIBase._ENDPOINT + "dataPackages"

    def __init__(self, key: str, product_id: str):
        super().__init__(product_id=product_id)
        self.key = key

    def __endpoint(self, api_name: str) -> str:
        return self._ENDPOINT + api_name + f"?key={self.key}"

    @classmethod
    def all_products(cls, key) -> list:
        """
        Returns a list of all available data packages

        Args:
            key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/

        Returns: A list of dictionaries containing all available Data Packages

        """
        print(cls._ENDPOINT + f"?key={key}")
        response = requests.get(cls._ENDPOINT + f"?key={key}")
        return response.json()

    @property
    @functools.lru_cache()
    def versions(self) -> list:
        """
        Get all the available versions for the data package
        """
        return requests.get(self._endpoint(f"{self.id}/versions")).json()

    @typechecked
    def product_list(self, version_id: str, file_name: str = None,
                     return_downloadobj: bool = False) -> Union[list, dict]:
        """
        Returns a list of possible downloads for a specific OS Premium Data Package based on given filters

        Args:
            version_id (str): Filter the list of possible downloads by the version id of the given product
            file_name (str, optional): Filter the list of downloads to only include those with this file name
            return_downloadobj (bool, optional): Returns the downloadable files as _DownloadObj objects instead of as a
                json. Defaults to False

        Returns:
            List of downloadable files from Downloads API
        """
        endpoint = self._endpoint(f"{self.id}/versions/{version_id}")
        params = {}
        if file_name:
            endpoint += "/downloads"
            params.update({"fileName": file_name})
            response = requests.get(url=endpoint, params=params)
            if return_downloadobj:
                return [_DownloadObj(url=response.json()["Location"], file_name=file_name,
                                     size=response.json()["Size"])]
        else:
            response = requests.get(url=endpoint, params=params)
            if return_downloadobj:
                return [_DownloadObj(url=download["url"], file_name=download["fileName"], size=response.json()["Size"])
                        for download in response.json()["downloads"]]

        return response.json()

    @typechecked
    def download(self,
                 version_id: str,
                 output_dir: Union[str, Path] = ".",
                 file_name: str = None,
                 download_multiple: bool = False,
                 overwrite: bool = False,
                 processes: int = None) -> list:
        """
        Downloads Data Package files to your local machine

        Args:
            version_id (str): The version id of the data package to download
            output_dir (Union[str, Path], optional): the path where the downloaded files will be saved. Defaults to
                current working directory
            file_name (str, optional): name of the file(s) to download
            download_multiple (bool, optional): whether to download multiple files if multiple products are within your
                search criteria. Defaults to False
            overwrite (bool, optional): whether to overwrite existing files. Defaults to False
            processes (int, optional): Number of processes with which to download multiple files. Only relevant if
                multiple files will be downloaded (and download_multiple is set to True)
        """
        download_list = self.product_list(version_id, file_name=file_name, return_downloadobj=True)
        return super()._download(download_list=download_list,
                                 output_dir=output_dir,
                                 overwrite=overwrite,
                                 download_multiple=download_multiple,
                                 processes=processes)
