import functools
import logging
from pathlib import Path
from typing import Union

import requests
from typeguard import typechecked
import osdatahub



from .downloads_api import _DownloadObj, _DownloadsAPIBase


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

    @classmethod
    def all_products(cls, key) -> list:
        """
        Returns a list of all available data packages

        Args:
            key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/

        Returns: A list of dictionaries containing all available Data Packages

        """
        response = osdatahub.get(cls._ENDPOINT, params={"key": key}, proxies=osdatahub.get_proxies())
        response.raise_for_status()
        content = response.json()
        if not content:
            logging.warning(f"You have no premium data packages available. "
                            f"Make sure that you first ordered a data package at "
                            f"https://osdatahub.os.uk/downloads/premium")
        return content

    @property
    @functools.lru_cache()
    def versions(self) -> list:
        """
        Get all the available versions for the data package
        """
        response = osdatahub.get(self._endpoint(f"{self._id}/versions"), params={"key": self.key}, proxies=osdatahub.get_proxies())
        response.raise_for_status()
        return response.json()

    @typechecked
    def product_list(self, version_id: str, return_downloadobj: bool = False) -> Union[list, dict]:
        """
        Returns a list of possible downloads for a specific OS Premium Data Package based on given filters

        Args:
            version_id (str): Filter the list of possible downloads by the version id of the given product
            return_downloadobj (bool, optional): Returns the downloadable files as _DownloadObj objects instead of as a
                json. Defaults to False

        Returns:
            List of downloadable files from Downloads API
        """
        endpoint = self._endpoint(f"{self._id}/versions/{version_id}")
        params = {"key": self.key}
        response = osdatahub.get(url=endpoint, params=params, proxies=osdatahub.get_proxies())
        response.raise_for_status()
        content = response.json()
        if not content:
            logging.warning(f"There are no premium data packages available with id={self.id} and "
                            f"version_id={version_id}. Make sure that you first ordered a data package at"
                            f"https://osdatahub.os.uk/downloads/premium")
        if return_downloadobj:
            return [_DownloadObj(url=download["url"], file_name=download["fileName"], size=download["size"])
                    for download in content["downloads"]]

        return content

    @typechecked
    def download(self,
                 version_id: str,
                 output_dir: Union[str, Path] = ".",
                 file_name: Union[str, None] = None,
                 overwrite: bool = False,
                 processes: Union[int, None] = None) -> list:
        """
        Downloads Data Package files to your local machine

        Args:
            version_id (str): The version id of the data package to download
            output_dir (Union[str, Path], optional): the path where the downloaded files will be saved. Defaults to
                current working directory
            file_name (str, optional): name of the file(s) to download
            overwrite (bool, optional): whether to overwrite existing files. Defaults to False
            processes (int, optional): Number of processes with which to download multiple files. Only relevant if
                multiple files will be downloaded (and download_multiple is set to True)
        """
        if file_name is not None:
            url = f'{self._endpoint(f"{self.id}/versions/{version_id}/downloads")}?fileName={file_name}&key={self.key}'
            return [_DownloadObj(url=url, file_name=file_name, size=0).download(output_dir=output_dir,
                                                                                overwrite=overwrite)]
        else:
            download_list = self.product_list(version_id, return_downloadobj=True)
            return super()._download(download_list=download_list,
                                     output_dir=output_dir,
                                     overwrite=overwrite,
                                     download_multiple=True,
                                     processes=processes)
