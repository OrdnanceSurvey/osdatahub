from typing import Union

from typing import Union

from geojson import FeatureCollection
from osdatahub.grow_list import GrowList
from shapely.geometry import LinearRing


def clean_features(feature_list: list, geom_type: str) -> list:
    """Post-processes API features to standardize geometry. In particular
    remove additional brackets and correct the nesting of
    brackets for multipolygons with holes.

    Args:
        feature_list (list): List of GeoJSON geometries
        geom_type (str): string describing which GeoJSON geometry type is
        in feature_list.

    Returns:
        list: cleaned GeoJSON geometries
    """
    if geom_type == "LineString":
        return clean_linestrings(feature_list)
    if geom_type == "Polygon":
        return clean_polygons(feature_list)
    return feature_list


def clean_linestrings(feature_list: list) -> list:
    """Post-process API LineStrings to standardize format by removing
    additional brackets.

    Args:
        feature_list (list): List of GeoJSON LineStrings

    Returns:
        list: List of GeoJSON LineStrings with extraneous brackets removed
    """
    return [clean_linestring(f) for f in feature_list]


def clean_linestring(feature: dict) -> dict:
    """Post-process API LineString to standardize format by removing
    additional brackets.

    Args:
        feature (dict): GeoJSON LineString feature

    Returns:
        dict: GeoJSON LineString feature with extraneous brackets removed
    """
    feature["geometry"]["coordinates"] = feature["geometry"]["coordinates"][0]
    return feature


def clean_polygons(feature_list: list) -> list:
    """Post-process API Polygons to fix geometries of MultiPolygons.

    Args:
        feature_list (list): List of GeoJSON Polygons

    Returns:
        list: List of fixed GeoJSON Polygons
    """
    return [clean_polygon(f) for f in feature_list]


def clean_polygon(feature: dict) -> dict:
    """Fixes the geometry of MultiPolygons, which are identified by being
    lists rather than dictionaries.

    Args:
        feature (dict): GeoJSON Polygon feature

    Returns:
        dict: Fixed GeoJSON Polygon feature
    """
    if isinstance(feature["geometry"], list):
        coordinates = feature["geometry"][0]["geometry"]["coordinates"]
        nested_polygons = nest_polygons(coordinates)
        feature["geometry"][0]["geometry"]["coordinates"] = nested_polygons
        feature["geometry"][0]["geometry"]["type"] = "MultiPolygon"
        return feature
    return feature


def nest_polygons(coordinates):
    """Checks if polygons are oriented clockwise or anticlockwise,
    and uses the order to assessemble polygons with holes in correctly.
    Only needed to correct multipolygons with holes.

    Args:
        coordinates (list): Coordinates in a clockwise orientation are exteriors,
    the following polygons of anticlockwise orientation are the holes for that
    polygons. Next clockwise coordinates are assumed to be exterior of new
    polygon.

    Returns:
        new_polys (list): A list of nested coordinates
    """
    new_polys = []
    polygon = []
    is_ccw = [LinearRing(coords).is_ccw for coords in coordinates]
    for direction, coords in zip(is_ccw, coordinates):
        if not direction:
            if polygon:
                new_polys.append(polygon)
            polygon = [coords]
        else:
            polygon.append(coords)
    new_polys.append(polygon)
    return new_polys


def features_to_geojson(feature_list, geom_type, crs) -> FeatureCollection:
    """Converts a list of GeoJSON gemetries to a FeatureCollection

    Args:
        feature_list (list): List of GeoJSON geometries
        geom_type (str): string describing which GeoJSON geometry type is
        in feature_list.
        crs (str): string representation of a coordinate system

    Returns:
        FeatureCollection: cleaned FeatureCollection
    """
    features = clean_features(feature_list, geom_type)
    return FeatureCollection(features, crs=crs)


def addresses_to_geojson(address_list, crs):
    """Converts a list of GeoJSON gemetries to a FeatureCollection, where the
    list of GeoJSONs represent addresses

    Args:
        address_list (list): List of GeoJSON addresses
        crs (str): string representation of a coordinate system

    Returns:
        FeatureCollection: cleaned FeatureCollection
    """
    features = [address_to_feature(address, crs) for address in address_list]
    return FeatureCollection(features, crs=crs)


def address_to_feature(address, crs):
    """The raw address from the PlacesAPI returns address in a JSON format where
    the coords have different keys depending on what CRS is requested. This
    function is needed to ensure that the keys of the coordinates are the same
    regardless of CRS.

    Args:
        address (dict): dictionary representation of an address
        crs (str): string representation of a coordinate system

    Returns:
        dict: dictionary representation of the input address

    Raises:
        ValueError: If CRS is not British National Grid, there should be
        attributes called 'LAT' and 'LNG' in the address
    """
    if crs.lower() in ("epsg:27700", "bng"):
        try:
            x, y = address["X_COORDINATE"], address["Y_COORDINATE"]
        except KeyError:
            x, y = address["GEOMETRY_X"], address["GEOMETRY_Y"]
    elif all(i in address.keys() for i in ("LNG", "LAT")):
        x, y = address["LNG"], address["LAT"]
    else:
        raise ValueError(
            f"If CRS is not British National Grid, there should be attributes called 'LAT' and 'LNG' in"
            f" address. LAT and LNG were not found, and CRS is {crs}"
        )

    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [x, y]},
        "properties": {**address},
    }


def validate_in_range(value: float, minimum: float, maximum: float) -> float:
    """Checks that the input value is between the maximum and minimum values
    and returns the original value if it is.

    Args:
        value (float): value to check
        minimum (float): minimum value in range (inclusive)
        maximum (float): maximum value in range (inclusive)

    Returns:
        float: returns input value if check passed

    Raises:
        ValueError: Value should be between {minimum} and {maximum}, got {value}.
    """
    if value < minimum or value > maximum:
        raise ValueError(f"Value should be between {minimum} and {maximum}, got {value}.")
    return value


def is_new_api(response: Union[dict, GrowList]) -> bool:
    """
    Checks whether the response came from the new API endpoint or the old API endpoint. The new endpoint response has
    2 differences: it includes a "crs" item in the response geojson and each feature contains a new property called
    'GmlID'. This function checks for these differences and returns a boolean.
    Args:
        response (Union[dict, GrowList]): response from the API. This could take any of 3 forms: the raw json response,
        a single feature, or a GrowList containing features.

    Returns (bool): True if response came from new endpoint, False otherwise
    """
    if isinstance(response, GrowList) and response:
        response = response.values[0]
    if "features" in response:
        return True if "crs" in response else False
    elif "geometry" in response and "properties" in response:
        return True if "GmlID" in response["properties"] else False
    else:
        raise ValueError("Unknown input. Must be either a FeatureCollection, a Feature as a dict, or a GrowList"
                         "containing features as dicts")
