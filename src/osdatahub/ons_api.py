import json

import osdatahub
import requests

ID_ENDPOINT = "http://statistics.data.gov.uk/geometry?resource=http://statistics.data.gov.uk/id/statistical-geography/"


def _sanitise_response(res: requests.Response) -> dict:
    res_body = res.text
    res_json = json.loads(res_body)
    res_json = _remove_duplicate_features(res_json)
    return res_json["features"][0]["geometry"]


def _remove_duplicate_features(response_json: dict) -> dict:
    """For some reason the API json response contains either 1 geomety or
        duplicates the same entry twice

    Args:
        response_json (dict): The json of the raw response from the ONS API

    Returns:
        response_json (dict): The json of the raw response with duplicates removed

    Raises:
        ValueError: If the raw response doesn't contain 1 or 2 features
    """
    if len(response_json["features"]) == 1:
        return response_json
    elif len(response_json["features"]) == 2:
        response_json["features"].pop(1)
        return response_json
    else:
        raise ValueError(f"Response JSON should contains either 1 or 2.")


def get_ons_geom(ons_code: str) -> dict:
    """Gets coordinates of the boundary of the polygon for the ons_code

    Args:
        ons_code (str): ONS code

    Returns:
        response_json (dict): The json of the raw response
    """
    url = f"{ID_ENDPOINT}{ons_code}"
    res = osdatahub.get(url, proxies=osdatahub.get_proxies())
    return _sanitise_response(res)
