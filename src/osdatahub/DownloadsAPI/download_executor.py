import logging
import os

import requests


class DownloadObj:
    def __init__(self, url, file_name):
        self.url = url
        self.file_name = file_name

    def download(self, output_dir: str, overwrite=False):

        output_path = os.path.join(output_dir, self.file_name)

        if os.path.isfile(output_path) and not overwrite:
            logging.warning(f"Overwrite is set to False and there is a file already in the location {output_path}. "
                            f"Skipping download...")
            return

        logging.info(f"Beginning download of {self.file_name}")
        r = requests.get(self.url, stream=True)
        if r.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        logging.info(f"Finished download to {output_path}")
        return output_path
