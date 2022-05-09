import functools
import logging
import os
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing import cpu_count
from pathlib import Path
from typing import Union

import requests
from tqdm import tqdm


class _DownloadObj:
    """ Helper class to download a file from Downloads API

    Args:
        url (str): Direct url for the download file
        file_name (str): Name of the file to be downloaded
    """

    def __init__(self, url: str, file_name: str, size: int):
        self.url = url
        self.file_name = file_name
        self.size = size

    def download(self, output_dir: Union[str, Path], overwrite: bool = False, pbar: tqdm = None) -> str:
        """
        Downloads file to given directory

        Args:
            output_dir (Union[str, Path]): Directory to save the downloaded file
            overwrite (bool, optional): whether to overwrite an existing file. Defaults to False
            pbar (tqdm, optional): tqdm progress bar to update in the event of downloading multiple files at once
        """
        output_path = os.path.join(output_dir, self.file_name)

        if os.path.isfile(output_path) and not overwrite:
            logging.warning(f"Overwrite is set to False and there is a file already in the location {output_path}. "
                            f"Skipping download...")
            return output_path

        r = requests.get(self.url, stream=True)
        r.raise_for_status()
        size = int(r.headers.get('content-length'))
        chunk_size = 1024
        if r.status_code == 200:
            with open(output_path, 'wb') as f:
                if not pbar:
                    pbar = tqdm(total=size, desc=self.file_name, unit="B", unit_scale=True, leave=True)
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    f.flush()
                    pbar.update(chunk_size)

        pbar.write(f"Finished downloading {self.file_name} to {output_path}")
        return output_path


class _DownloadsAPIBase(ABC):
    """Parent class for Product and DataPackage classes as part of the DownloadsAPI
    (https://osdatahub.os.uk/docs/downloads/overview)

    Args:
        product_id (str): Valid ID for a Downloads API Product or DataPackage.

    """
    _ENDPOINT = f"https://api.os.uk/downloads/v1/"

    def __init__(self, product_id: str):
        self._id = product_id

    def _endpoint(self, api_name: str) -> str:
        """
        Adds the api to the base endpoint

        Args:
            api_name (str): API endpoint to add to _ENDPOINT attribute

        Returns:
            str: concatenated endpoint consisting of _ENDPOINT and api_name
        """
        return f"{self._ENDPOINT}/{api_name}"

    @property
    def id(self):
        return self._id

    @property
    @functools.lru_cache()
    def details(self) -> dict:
        """
        Calls endpoint to return details about the product or data package
        """
        response = requests.get(self._endpoint(self._id))
        response.raise_for_status()
        return response.json()

    @classmethod
    def all_products(cls, **kwargs) -> list:
        """
        Returns a list of all available products of the product type

        Returns: list of dictionaries containing all products available to download

        """
        response = requests.get(cls._ENDPOINT)
        response.raise_for_status()
        return response.json()

    @abstractmethod
    def product_list(self):
        """
        Abstract method for returning a list of files available to download for a specific data package/opendata product
        Returns:

        """
        pass

    @staticmethod
    def _download(download_list: Union[list, _DownloadObj], output_dir: Union[str, Path], overwrite: bool = False,
                  download_multiple: bool = False, processes: int = None) -> list:
        """
        Downloads product/datapackage to the given directory. Can download a single format or can download multiple
        formats in parallel

        Args:
             download_list (Union[list, DownloadObj]): The DownloadObj objects representing all the
                products/data packages that need to be downloaded
             output_dir (Union[str, Path]): path to directory where the files will be saved to
             overwrite (bool, optional): Whether to overwrite any existing files with the same name and path.
                Defaults to False
             download_multiple (bool, optional): Whether to download multiple files, generally the same data but in
                different formats. Defaults to False
             processes (int, optional): If downloading multiple files, the number of parallel processes to be used.
                defaults to the machine's CPU count
        """
        if isinstance(download_list, list) and len(download_list) == 0:
            raise Exception("Argument \"download_list\" is empty. Please provide at least one DownloadObj to download")
        elif isinstance(download_list, list) and len(download_list) > 1 and not download_multiple:
            raise Exception("Argument \"download_list\" contains more than 1 object to download, but argument "
                            "\"download_multiple\" is set to False. Please pass only 1 download or set "
                            "\"download_multiple\" to True.")

        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        # downloads in parallel if multiple files need to be downloaded
        if isinstance(download_list, list) and len(download_list) > 1 and download_multiple:
            if not processes:
                processes = cpu_count()
            with ThreadPoolExecutor(max_workers=processes) as executor:
                pbar = tqdm(total=sum([d.size for d in download_list]), unit="B", unit_scale=True, leave=True,
                            desc=f"Downloading {len(download_list)} files from osdatahub")
                results = list([executor.submit(p.download, output_dir, overwrite, pbar) for p in download_list])

                num_downloads_completed = 0
                for _ in as_completed(results):
                    num_downloads_completed += 1
                    pbar.set_description(
                        f"Downloading {len(download_list) - num_downloads_completed} files from osdatahub")
        else:
            # download single file
            d = download_list[0] if isinstance(download_list, list) else download_list
            results = [d.download(output_dir, overwrite)]

        return results
