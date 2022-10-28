import re
from collections import namedtuple

Dataset = namedtuple("Dataset", "name short_code")

# TODO: add rest of collections
COLLECTIONS = {
    "buildingline": Dataset("Building Line", "bld-fts-buildingline"),
    "buildingpart": Dataset("Building Part", "bld-fts-buildingpart"),
    "namedarea": Dataset("Named Area", "gnm-fts-namedarea"),
    "namedpoint": Dataset("Named Point", "gnm-fts-namedpoint"),
}

SHORT_CODES = {
    "bld": {
        "fts": {
            "buildingline": COLLECTIONS["buildingline"],
            "buildingpart": COLLECTIONS["buildingpart"]
        }
    }
}


def preformat_collection(col: str) -> str:
    if re.match(r"/(\w+-\w+-\w+)/", col):
        col = col.split("-")[-1]
    elif re.match(r"/(\w+_\w+)", col):
        col = col.replace("_", "")

    return col


def validate_collection(col: str) -> bool:
    return preformat_collection(col) in COLLECTIONS


def get_collection(col: str) -> str:
    col = preformat_collection(col)

    if col in COLLECTIONS:
        return COLLECTIONS[col]
    else:
        raise ValueError(f"Unknown collection {col}")
