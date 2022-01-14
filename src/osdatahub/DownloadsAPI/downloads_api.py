import functools
import logging
import os.path
from os import environ
from dataclasses import dataclass
from typing import Optional, Union, Iterable
from multiprocessing.pool import ThreadPool


import requests
from typeguard import typechecked

from osdatahub.codes import AREA_CODES


class DownloadsAPI:
    _ENDPOINT = f"https://api.os.uk/downloads/v1/"

    def __init__(self, key, id):
        self.key = key
        self.id = id

    def _endpoint(self, api_name: str) -> str:
        return f"{self._ENDPOINT}/{api_name}"

    @functools.cached_property
    def details(self):
        return requests.get(self._endpoint(self.id)).json()

    @classmethod
    def all_products(cls) -> list:
        response = requests.get(cls._ENDPOINT)
        return response.json()

    def download(self, urls: Union[Iterable, str]):
        results = ThreadPool(8).imap_unordered(fetch_url, urls)
        for path in results:
            print(path)
