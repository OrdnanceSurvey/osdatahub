from typing import Union
# import re

EPSG = {
    "epsg:4326": "http://www.opengis.net/def/crs/EPSG/0/4326",
    "epsg:27700": "http://www.opengis.net/def/crs/EPSG/0/27700",
    "epsg:3857": "http://www.opengis.net/def/crs/EPSG/0/3857",
    "epsg:7405": "http://www.opengis.net/def/crs/EPSG/0/7405",
    "crs84": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"
}

def get_crs(crs: Union[str,int] = None, valid_crs: Union[list, tuple] = EPSG.keys()) -> str:
    if not set(valid_crs).issubset(set(EPSG)):
        raise ValueError(f"`valid_crs` parameter is not valid. Must be an iterable containing only {EPSG.keys()} but "
                         f"had value {valid_crs}")

    if isinstance(crs, int):
        crs = f"epsg:{crs}"

    crs = crs.lower()
    if crs in EPSG and crs in valid_crs:
        return EPSG[crs]  
    else:
        #Checks if the url provided is or closely corresponds to a valid crs url as defined by NGD API spec
        for key, url in EPSG.items():
            if url[7:].casefold() in crs.casefold() and len(crs)<50:
                crs = key
                return EPSG[crs]

    raise ValueError(f'Unknown CRS. Must be in format "epsg:4326", "EPSG:4326", 4326, or '
                     f'"http://www.opengis.net/def/crs/EPSG/0/4326". See documentation for available crs.')
