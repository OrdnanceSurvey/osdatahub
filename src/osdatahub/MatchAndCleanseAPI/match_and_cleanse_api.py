from collections.abc import Iterable
from typing import Union
from typeguard import typechecked

from osdatahub.codes import DATASET
from osdatahub.grow_list import GrowList


class MatchAndCleanseAPI:
    """Main class for querying the OS Match & Cleanse API (https://osdatahub.os.uk/docs/match/overview)

    """
    __ENDPOINT = r"https://api.os.uk/search/match/v1/"
    HEADERS = {"method": "POST",
               "headers": "{'Content-Type': 'application/json'}"}

    def __init__(self, key: str):
        self.key = key

    def __endpoint(self, api_name: str) -> str:
        return self.__ENDPOINT + api_name + f"?key={self.key}"

    @typechecked
    def match(self, text: str,
              limit: int = 100,
              dataset: Union[Iterable, str] = None,
              minmatch: float = None,
              matchprecision: str = None,
              classification_code: Union[Iterable, str] = None,
              logical_status_code: Union[str, int] = None,
              country_code: Union[str, Iterable] = None,
              output_srs: str = None):
        """

        """
        data = GrowList()
        params = {"query": text}

        if dataset:
            dataset = set(dataset) if isinstance(dataset, Iterable) else {dataset}
            if not dataset.issubset(DATASET):
                raise ValueError(f"Invalid dataset values. Possible values are {DATASET}")
        try:
            n_required = min(limit, 100)
            while n_required > 0 and data.grown:
                params.update({"offset": len(data), "maxresults": n_required})
                print(params)
                response = requests.get(self.__endpoint("find"), params=params)
                data.extend(self.__format_response(response))
                n_required = min(100, limit - len(data))
        except KeyError:
            response.raise_for_status()
        return addresses_to_geojson(data.values, "EPSG:27700")
