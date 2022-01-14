from typing import Union, Iterable

LOGICAL_STATUS_CODES = {
    1: "Approved address",
    3: "Alternate address",
    6: "Provisional address",
    8: "Historic address"
}


def validate_logical_status_code(logical_status_code: Union[str, int]) -> bool:
    return logical_status_code in LOGICAL_STATUS_CODES.keys()


COUNTRY_CODES = {
    "E": "This record is within England",
    "W": "This record is within Wales",
    "S": "This record is within Scotland",
    "N": "This record is within Northern Island",
    "L": "This record is within Channel Islands",
    "M": "This record is within the Isle of Man",
    "J": "This record is not assigned to a country as it falls outside of the land boundaries used"
}

AREA_CODES = {"GB", "HP", "HT", "HU", "HW", "HX", "HY", "HZ", "NA", "NB", "NC", "ND", "NF", "NG", "NH", "NJ", "NK",
              "NL", "NM", "NN," "NO", "NR", "NS", "NT", "NU", "NW", "NX", "NY", "NZ", "OV", "SD", "SE", "TA", "SH",
              "SJ", "SK", "TF", "TG", "SM", "SN", "SO", "SP", "TL", "TM", "SR", "SS", "ST", "SU", "TQ", "TR", "SV",
              "SW", "SX", "SY", "SZ", "TV"}


def validate_country_codes(country_code: Union[Iterable, str]) -> set:
    country_code = set(country_code) if isinstance(country_code, Iterable) else {country_code}
    return country_code - set(COUNTRY_CODES.keys())


DATASET = {
    "DPA",
    "LPI"
}
