import functools
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool

import requests
from tqdm import tqdm


class DownloadsAPI:
    _ENDPOINT = f"https://api.os.uk/downloads/v1/"

    def __init__(self, key, product_id):
        self.key = key
        self.id = product_id
        self.filters = []

    def _endpoint(self, api_name: str) -> str:
        return f"{self._ENDPOINT}/{api_name}"

    @functools.cached_property
    def details(self):
        return requests.get(self._endpoint(self.id)).json()

    @classmethod
    def all_products(cls) -> list:
        # TODO: return each entry as the desired object
        response = requests.get(cls._ENDPOINT)
        return response.json()

    def download(self, download_list, output_dir, overwrite=False, download_multiple=False, processes=None):
        if len(download_list) == 0:
            raise Exception("Nothing is gonna download")
        elif len(download_list) > 1 and not download_multiple:
            raise Exception("Too many")

        if len(download_list) > 1 and download_multiple:
            if not processes:
                processes = cpu_count()
            with ThreadPool(processes) as pool:
                results = tqdm(pool.imap_unordered(lambda p: p.download(output_dir=output_dir, overwrite=overwrite),
                                                   download_list), total=len(download_list))
        else:
            results = download_list[0].download(output_dir, overwrite)

        return results
