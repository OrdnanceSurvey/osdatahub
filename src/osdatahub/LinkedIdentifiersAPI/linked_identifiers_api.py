from typing import Union

import requests
from typeguard import typechecked

import osdatahub
from osdatahub.errors import raise_http_error
from osdatahub.LinkedIdentifiersAPI.linked_identifier_options import (
    correlation_methods, feature_types, identifier_types)


class LinkedIdentifiersAPI:
    """Main class for querying the OS Linked Identifiers API (https://osdatahub.os.uk/docs/linkedIdentifiers/overview)

    Args:
        key (str): A valid OS API Key. Get a free key here - https://osdatahub.os.uk/

    Example::

        from osdatahub import LinkedIdentifiersAPI
        from os import environ

        key = environ.get("OS_API_KEY")
        linked_ids = LinkedIdentifiersAPI(key)
        results = linked_ids.query(200001025758)
    """

    __ENDPOINT = r"https://api.os.uk/search/links/v1/"

    def __init__(self, key: str):
        self.key = key

    @staticmethod
    def __request(endpoint: str) -> dict:
        response = osdatahub.get(endpoint, proxies=osdatahub.get_proxies())
        if response.status_code != 200:
            raise_http_error(response)
        return response.json()

    def __get_endpoint(
            self, identifier: Union[int, str], feature_type: str, identifier_type: str
    ) -> str:
        if feature_type is not None and identifier_type is not None:
            raise ValueError(
                "It is possible to query by the feature_type "
                + "OR the identifier type, but not both"
            )
        elif feature_type is not None:
            feature_types.validate(feature_type)
            subdirectory = f"featureTypes/{feature_type}"
        elif identifier_type is not None:
            identifier_types.validate(identifier_type)
            subdirectory = f"identifierTypes/{identifier_type}"
        else:
            subdirectory = "identifiers"
        return self.__ENDPOINT + subdirectory + f"/{identifier}?key={self.key}"

    @typechecked
    def query(
            self,
            identifier: Union[int, str],
            feature_type: str = None,
            identifier_type: str = None,
    ) -> dict:
        """Run a query of the OS Linked Identifiers API - looks up an
        identifier and finds its associated identifiers.

        Queries can be also be made more specific if the feature type
        or identifier type are known, but note: you cannot specify both!

        Args:
            identifier (Union[int, str]): The identifier to look up.
            feature_type (str): Look up linked identifiers when the input feature type is known.
            identifier_type (str): Look up linked identifiers when the input identifier type is known.

        Returns:
            dict: The results of the query in JSON format
        """
        endpoint = self.__get_endpoint(identifier, feature_type, identifier_type)
        return self.__request(endpoint)

    @typechecked
    def product_version(self, correlation_method: str) -> dict:
        """Discover the current product version information. For a list of
        valid correlation methods see (https://osdatahub.os.uk/docs/linkedIdentifiers/technicalSpecification)

        Args:
            correlation_method (str): Correlation method - corresponding to a
            particular feature relationship

        Returns:
            dict: The results of the query in JSON format
        """
        correlation_methods.validate(correlation_method)
        endpoint = (
                self.__ENDPOINT + f"productVersionInfo/{correlation_method}?key={self.key}"
        )
        return self.__request(endpoint)
