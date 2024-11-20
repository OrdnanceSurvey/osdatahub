from pathlib import Path
from typing import Union

import requests
from typeguard import typechecked

import osdatahub
from osdatahub.codes import AREA_CODES

from .downloads_api import _DownloadObj, _DownloadsAPIBase


class OpenDataDownload(_DownloadsAPIBase):
    """
    Main class for downloading OS OpenData products
    (https://osdatahub.os.uk/docs/downloads/technicalSpecification#/OS%20OpenData)

    Args:
        product_id (str): Valid ID for a Downloads API Product or DataPackage.
    """
    _ENDPOINT = _DownloadsAPIBase._ENDPOINT + "products"

    # TODO: change name
    @typechecked
    def product_list(self, 
                     file_name: Union[str, None] = None, 
                     file_format: Union[str, None] = None, 
                     file_subformat: Union[str, None] = None,
                     area: Union[str, None] = None, 
                     return_downloadobj: bool = False) -> Union[list, dict]:
        """
        Returns a list of possible downloads for a specific OS OpenData Product based on given filters

        Args:
            file_name (str, optional): Filter the list of downloads to only include those with this file name
            file_format (str, optional): Filter the list of downloads to only include those with this format
            file_subformat (str, optional): Filter the list of downloads to only include those with this subformat
            area (str, optional) Filter the list of downloads to only include those that cover this area. Available
                values can be found `here <https://osdatahub.os.uk/docs/downloads/technicalSpecification#/OS%20OpenData/get_products__productId__downloads>`_
            return_downloadobj (bool, optional): Returns the downloadable files as _DownloadObj objects instead of as a
                json. Defaults to False

        Returns:
            List of downloadable files from Downloads API
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

        response = osdatahub.get(url=self._endpoint(f"{self._id}/downloads"), params=params, proxies=osdatahub.get_proxies())
        response.raise_for_status()
        if return_downloadobj:
            return [_DownloadObj(url=download["url"], file_name=download["fileName"], size=download["size"])
                    for download in response.json()]
        else:
            return response.json()

    def download(self, 
                 output_dir: Union[str, Path] = ".",
                 file_name: Union[str, None] = None,
                 file_format: Union[str, None] = None,
                 file_subformat: Union[str, None] = None,
                 area: Union[str, None] = None,
                 download_multiple: bool = False,
                 overwrite: bool = False,
                 processes: Union[int, None] = None) -> list:
        """
        Downloads Product files to your local machine

        Args:
            output_dir (Union[str, Path], optional): the path where the downloaded files will be saved. Defaults to
                current working directory
            file_name (str, optional): name of the file(s) to download
            file_format (str, optional): format of the file(s) to download
            file_subformat (str, optional): subformat of the file(s) to download
            area (str, optional): The area that the file must cover. Available values can be found in
                osdatahub.codes.AREA_CODES or on the `OS Data Hub website <https://osdatahub.os.uk/docs/downloads/technicalSpecification#/OS%20OpenData/get_products__productId__downloads>`_
            download_multiple (bool, optional): whether to download multiple files if multiple products are within your
                search criteria. Defaults to False
            overwrite (bool, optional): whether to overwrite existing files. Defaults to False
            processes (int, optional): Number of processes with which to download multiple files. Only relevant if
                multiple files will be downloaded (and download_multiple is set to True)
        """
        download_list = self.product_list(file_name=file_name, file_format=file_format, file_subformat=file_subformat,
                                          area=area, return_downloadobj=True)
        return super()._download(download_list=download_list,
                                 output_dir=output_dir,
                                 overwrite=overwrite,
                                 download_multiple=download_multiple,
                                 processes=processes)
