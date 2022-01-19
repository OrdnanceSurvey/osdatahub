from typing import Union

import requests
from osdatahub.errors import raise_http_error
from osdatahub.LinkedIdentifiersAPI.linked_identifier_options import (
    correlation_methods, feature_types, identifier_types)


class LinkedIdentifiersAPI:

    __ENDPOINT = r"https://api.os.uk/search/links/v1/"

    def __init__(self, key: str):
        self.key = key
        
    def __request(self, endpoint: str) -> dict:
        response = requests.get(endpoint)
        if response.status_code != 200:
            raise_http_error(response)
        return response.json()

    def __get_endpoint(self, id: Union[int, str],
                       feature_type: str, identifier_type: str) -> str:
        if feature_type is not None and identifier_type is not None:
            raise ValueError("It is possible to query by the feature_type " +\
                             "OR the identifier type, but not both")
        elif feature_type is not None:
            feature_types.validate(feature_type)
            query = f"featureTypes/{feature_type}/{id}?key={self.key}"
        elif identifier_type is not None:
            identifier_types.validate(identifier_type)
            query = f"identifierTypes/{identifier_type}/{id}?key={self.key}"
        else:
            query = f"identifiers/{id}?key={self.key}"
        return self.__ENDPOINT + query

    def lookup(self, id: Union[int, str],
               feature_type: str = None, identifier_type: str = None) -> dict:
        endpoint = self.__get_endpoint(id, feature_type, identifier_type)
        return self.__request(endpoint)

    def product_version(self, correlation_method: str) -> dict:
        correlation_methods.validate(correlation_method)
        endpoint = self.__ENDPOINT +\
            f"productVersionInfo/{correlation_method}?key={self.key}"
        return self.__request(endpoint)


if __name__ == "__main__":
    import os

    key = os.environ.get("OS_API_KEY")

    linked_id = LinkedIdentifiersAPI(key)

    print(linked_id.lookup("200001025758", identifier_type="UPRN"))
