import functools
import json
import logging
import os
import time
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from http import HTTPStatus
from multiprocessing import cpu_count
from pathlib import Path
from typing import List, Union

import requests
from requests.exceptions import HTTPError
from tqdm import tqdm

import osdatahub

retries = 3


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

    def download(self, 
                 output_dir: Union[str, Path], 
                 overwrite: bool = False, 
                 pbar: Union[tqdm, None] = None) -> str:
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

        for _ in range(retries):
            try:
                response = requests.get(
                    self.url, stream=True, proxies=osdatahub.get_proxies())
                response.raise_for_status()
                expected_size = int(response.headers.get('content-length'))
                current_size = 0
                chunk_size = 1048576  # 1024 ** 2 -> 1MB
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        if not pbar:
                            pbar = tqdm(
                                total=expected_size, desc=self.file_name, unit="B", unit_scale=True, leave=True)
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            current_size += len(chunk)
                            f.write(chunk)
                            f.flush()
                            pbar.update(chunk_size)
                        if expected_size != current_size:
                            deficit = expected_size - current_size
                            raise IOError(
                                f'incomplete read ({current_size} bytes read, {deficit} more expected)'
                            )
                        pbar.write(
                            f"Finished downloading {self.file_name} to {output_path}")
                break

            except HTTPError as exc:
                if int(exc.response.status_code) == 429:
                    time.sleep(20)
                    continue
                raise

        return output_path


def remove_key(url: str):
    """Remove key from url
    """
    return "".join([section for section in url.split("&") if "key" not in section])


def format_missing_files(missing_files: List[_DownloadObj]) -> List[dict]:
    """Convert download objects to dictionaries and sanitise
    """
    file_info = []
    for _download_obj in missing_files:
        info = _download_obj.__dict__
        info['url'] = remove_key(info['url'])
        file_info.append(info)
    return {
        "missing_file_count": len(missing_files),
        "missing_file_info": file_info
    }


def save_missing_files(missing_files: List[_DownloadObj], output_dir: Union[str, Path]) -> None:
    """Format and save missing files 
    """
    if len(missing_files) == 0:
        return
    data = format_missing_files(missing_files)
    path = os.path.join(
        output_dir, f"missing_files.{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    json.dump(data, open(path, "w"))


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
        response = osdatahub.get(self._endpoint(
            self._id), proxies=osdatahub.get_proxies())
        response.raise_for_status()
        return response.json()

    @classmethod
    def all_products(cls, **kwargs) -> list:
        """
        Returns a list of all available products of the product type

        Returns: list of dictionaries containing all products available to download

        """
        response = osdatahub.get(
            cls._ENDPOINT, proxies=osdatahub.get_proxies())
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
    def _download(download_list: Union[list, _DownloadObj], 
                  output_dir: Union[str, Path], 
                  overwrite: bool = False,
                  download_multiple: bool = False, 
                  processes: Union[int, None] = None) -> list:
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
            raise Exception(
                "Argument \"download_list\" is empty. Please provide at least one DownloadObj to download")
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
                            desc=f"Downloaded 0/{len(download_list)} files from osdatahub")

                processed_downloads = {}
                num_downloads_completed = 0
                results = []
                missing_files = []

                for p in download_list:
                    future = executor.submit(
                        p.download, output_dir, overwrite, pbar)
                    processed_downloads[future] = p

                for future in as_completed(processed_downloads):
                    info = processed_downloads[future]
                    try:
                        results.append(future.result())
                        num_downloads_completed += 1
                        pbar.set_description(
                            f"Downloaded {num_downloads_completed}/{len(download_list)} files from osdatahub")
                    except Exception:
                        missing_files.append(info)

                save_missing_files(missing_files, output_dir)
        else:
            # download single file
            d = download_list[0] if isinstance(
                download_list, list) else download_list
            results = [d.download(output_dir, overwrite)]

        return results
