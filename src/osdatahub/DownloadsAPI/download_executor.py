import logging
import multiprocessing
import os
from multiprocessing.pool import ThreadPool
from typing import Iterable, Union
from tqdm import tqdm

import requests


class Download:
    def __init__(self, url, file_name, file_format: str = None, output_path: str = None):
        self.url = url
        self.file_name = file_name
        self.format = file_format if file_format else os.path.splitext(self.file_name)[1][1:]
        if output_path:
            # if output path is a directory, name output file the same as file_name attribute
            _, extension = os.path.splitext(output_path)
            if not extension:
                os.makedirs(output_path)
                self.output_path = os.path.join(output_path, self.file_name)
            else:
                self.output_path = output_path
        else:
            self.output_path = self.file_name

    def download(self, overwrite=False):

        if os.path.isfile(self.output_path) and not overwrite:
            logging.warning(f"Overwrite is set to False and there is a file already in the location {self.output_path}. "
                            f"Skipping download...")
            return

        logging.info(f"Beginning download of {self.file_name}")
        r = requests.get(self.url, stream=True)
        if r.status_code == 200:
            with open(self.output_path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        logging.info(f"Finished download to {self.output_path}")
        return self.output_path


def download_products(products: Union[tuple, list, set, Download], overwrite: bool = False, processes: int = None):
    if isinstance(products, Download):
        results = products.download()
    else:
        if not processes:
            processes = multiprocessing.cpu_count()
        with ThreadPool(processes) as p:
            results = tqdm(p.imap_unordered(lambda p: p.download(overwrite=overwrite), products), total=len(products))

    return results
