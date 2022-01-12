from collections.abc import Iterable
from typing import Union

import requests
from typeguard import typechecked

from osdatahub.codes import DATASET, validate_logical_status_code, validate_country_codes, COUNTRY_CODES, \
    LOGICAL_STATUS_CODES
from osdatahub.grow_list import GrowList
from osdatahub.utils import addresses_to_geojson


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
              output_crs: str = "EPSG:27700",
              dataset: Union[Iterable, str] = None,
              min_match: Union[float, int] = None,
              match_precision: Union[int, str] = None,
              classification_code: Union[Iterable, str] = None,
              logical_status_code: Union[str, int] = None,
              country_code: Union[str, Iterable] = None):
        """

        """
        data = GrowList()
        params = {"query": text}

        if not limit > 0:
            raise ValueError(f"Argument \"limit\" must have a positive value")

        if dataset:
            dataset = set([dataset] if isinstance(dataset, str) else dataset)
            if not all(isinstance(x, str) for x in dataset):
                raise TypeError("Argument \"dataset\" must consist only of strings")
            elif not dataset.issubset(DATASET):
                raise ValueError(f"Invalid dataset values. Possible values are {DATASET} but had value {dataset}")
            params.update({"dataset": ",".join(sorted(dataset))})

        if min_match is not None:
            if not 0.1 <= min_match <= 1:
                raise ValueError(f"argument \"min_match\" must have a value between 0.1 and 1. Had a value {min_match}")
            params.update({"minmatch": min_match})

        if match_precision is not None:
            if (isinstance(match_precision, str) and not match_precision.isnumeric()) or \
                    (not 1 <= int(match_precision) <= 10):
                raise ValueError(f"argument \"match_precision\" must be a number between 1 and 10, but had a value of "
                                 f"{match_precision}")
            params.update({"matchprecision": str(match_precision)})

        if classification_code or logical_status_code or country_code:
            params.update({"fq": self.__format_fq(classification_code, logical_status_code, country_code)})

        if output_crs:
            if output_crs not in ('BNG', 'EPSG:27700', 'WGS84', 'EPSG:4326', 'EPSG:3857', 'EPSG:4258'):
                raise ValueError(f"argument \"output_srs\" must have be one of 'BNG', 'EPSG:27700', 'WGS84', "
                                 f"'EPSG:4326', 'EPSG:3857', 'EPSG:4258' but had a value of {output_crs}")
            params.update({"output_srs": output_crs})

        try:
            n_required = min(limit, 100)
            while n_required > 0 and data.grown:
                params.update({"offset": len(data), "maxresults": n_required})
                response = requests.get(self.__endpoint("match"), params=params)
                data.extend(self.__format_response(response))
                n_required = min(100, limit - len(data))
        except KeyError:
            response.raise_for_status()
        print(data.values)
        return addresses_to_geojson(data.values, output_crs)

    @staticmethod
    @typechecked
    def __format_fq(classification_code: Union[str, Iterable] = None,
                    logical_status_code: Union[str, int] = None,
                    country_code: Union[str, Iterable] = None) -> list:
        """
        Formats optional fq arguments for Match & Cleanse API query

        Args:
            classification_code (str|Iterable[str], optional): The classification codes to filter query
            logical_status_code (str|Number, optional): Logical status code to filter query
            country_code (str|Iterable[str], optional): Country code to filter query

        Returns:
            list of fq filtering arguments
        """
        fq_args = []
        if classification_code:
            if isinstance(classification_code, str):
                class_codes = "CLASSIFICATION_CODE:" + classification_code
            elif isinstance(classification_code, Iterable):
                if not all(isinstance(x, str) for x in classification_code):
                    raise TypeError("Argument \"classification_code\" must consist only of strings")
                class_codes = " ".join([f"CLASSIFICATION_CODE:{arg}" for arg in classification_code])
            else:
                raise TypeError(f"'classification_code' argument must be Iterable or str, but was type "
                                f"{type(classification_code)}")

            fq_args.append(class_codes)
        if logical_status_code:
            if not str(logical_status_code).isnumeric():
                raise TypeError("logical_status_code can have a maximum of 1 filter and must have a numeric value.")
            if not validate_logical_status_code(logical_status_code):
                raise ValueError(f"argument \"logical_status_code\" must be one of {LOGICAL_STATUS_CODES} but was "
                                 f"{logical_status_code}")
            fq_args.append("LOGICAL_STATUS_CODE:" + str(logical_status_code))

        if country_code:
            invalid_country_codes = validate_country_codes(country_code)
            if invalid_country_codes:
                raise ValueError(f"Argument \"country_code\" must contain only the values {COUNTRY_CODES.keys()} but "
                                 f"had the invalid values {invalid_country_codes}")

            if isinstance(country_code, str):
                country_codes_str = "COUNTRY_CODE:" + country_code
            elif isinstance(country_code, Iterable):
                if not all(isinstance(x, str) for x in country_code):
                    raise TypeError("Argument \"country_code\" must consist only of strings")
                country_codes_str = " ".join([f"COUNTRY_CODE:{arg}" for arg in country_code])
            else:
                raise TypeError(f"'country_code' argument must be Iterable or str, but was type {type(country_code)}")

            fq_args.append(country_codes_str)

        return fq_args

    @staticmethod
    def __format_response(response: requests.Response) -> list:
        return [result["DPA"] for result
                in response.json()["results"]]
