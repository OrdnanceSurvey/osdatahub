from enum import Enum
from typing import Union
from urllib.parse import urlparse

EPSG = {
    "epsg:4326": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "epsg:27700": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "epsg:3857": "http://www.opengis.net/def/crs/EPSG/0/3857",
    "epsg:7405": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "crs84": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
}


# TODO: add url possibility
def get_crs(crs: str = None, epsg: int = None, valid_crs: list[str] = EPSG.keys()) -> str:
    if crs and epsg:
        raise ValueError("Must pass either crs or epsg, but not both")
    if epsg:
        crs = f"epsg:{epsg}"

    if crs in EPSG and crs in valid_crs:
        return EPSG[crs.lower()]
    
    raise ValueError("Unknown CRS. Must be...")
    

