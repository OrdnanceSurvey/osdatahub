from collections import namedtuple

Dataset = namedtuple("Dataset", "name short_code")

# TODO: add rest of collections
# TODO: change datasets to collections
DATASETS = {
    "building_line": Dataset("Building Line", "bld-fts-buildingline"),
    "building_part": Dataset("Building Part", "bld-fts-buildingpart"),
    "named_area": Dataset("Named Area", "gnm-fts-namedarea"),
    "named_point": Dataset("Named Point", "gnm-fts-namedpoint"),

}

SHORT_CODES = {
    "bld": {
        "fts": {
            "buildingline": DATASETS["building_line"],
            "buildingpart": DATASETS["building_part"]
        }
    }
}


def validate_collection(col: str):
    # TODO: implement validate_collection()
    pass


def get_collection(col: str):
    # TODO: implement get_collection()
    pass
