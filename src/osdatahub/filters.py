from typing import Callable, Union
from enum import Enum
from osdatahub import Extent


def spatial_filter(operator: str, extent: Extent) -> str:
    """Constructs an OGC XML filter using the given operator string and the given extent

    Args:
        operator (str): Case-sensitive name of operator for OGC filter string
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    coords = extent.xml_coords
    crs = extent.crs.upper()
    return (
        f"<ogc:{operator}>"
        "<ogc:PropertyName>SHAPE</ogc:PropertyName>"
        f"<gml:Polygon xmlns:gml='http://www.opengis.net/gml' srsName='{crs}'>"
        "<gml:outerBoundaryIs>"
        "<gml:LinearRing>"
        f'<gml:coordinates decimal="." cs="," ts=" ">{coords}</gml:coordinates>'
        "</gml:LinearRing>"
        "</gml:outerBoundaryIs>"
        "</gml:Polygon>"
        f"</ogc:{operator}>"
    )


def intersects(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that intersects the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Intersects", extent)


def touches(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that touches the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Touches", extent)


def disjoint(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that does not interact with the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Disjoint", extent)


def contains(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that contains the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Contains", extent)


def within(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that is within the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Within", extent)


def crosses(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that crosses the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Crosses", extent)


def overlaps(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that overlaps the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Overlaps", extent)


def equals(extent: Extent) -> str:
    """Constructs an OGC XML filter for data that is equal to the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        str: A valid OGC XML filter
    """
    return spatial_filter("Equals", extent)


def single_attribute_filter(property_name, filter_name, value):
    return (
        f"<ogc:{filter_name}>"
        f"<ogc:PropertyName>{property_name}</ogc:PropertyName>"
        f"<ogc:Literal>{value}</ogc:Literal>"
        f"</ogc:{filter_name}>"
    )


def is_between(property_name: str, lower: float, upper: float) -> str:
    """Constructs an OGC XML filter for a numerical attribute between 2 values

    Args:
        property_name (str): Property / attribute name to be filtered
        lower (float): The filter's lower bound
        upper (float): The filter's upper bound

    Returns:
        str: A valid OGC XML filter
    """
    return (
        f"<ogc:PropertyIsBetween>"
        f"<ogc:PropertyName>{property_name}</ogc:PropertyName>"
        f"<LowerBoundary>"
        f"<ogc:Literal>{lower}</ogc:Literal>"
        "</LowerBoundary>"
        "<UpperBoundary>"
        f"<ogc:Literal>{upper}</ogc:Literal>"
        "</UpperBoundary>"
        f"</ogc:PropertyIsBetween>"
    )


def is_like(
    property_name: str,
    value: str,
    wildcard: str = "*",
    single_char: str = "#",
    escape_char: str = "!",
) -> str:
    """Constructs an OGC XML filter for a string attribute that is similar to
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (str): String that is used to match with attribute values
        wildcard (str, optional): A character that any combination of other
            characters will match with. Defaults to "*".
        single_char (str, optional): A character that any single character
            will match with. Defaults to "#".
        escape_char (str, optional): Used to escape the meaning of the
            wildcard, single_char and escape_char itself. Defaults to "!".

    Returns:
        str: A valid OGC XML filter
    """
    return (
        f'<ogc:PropertyIsLike wildCard="{wildcard}" singleChar="{single_char}" escapeChar="{escape_char}">'
        f"<ogc:ValueReference>{property_name}</ogc:ValueReference>"
        f"<ogc:Literal>{value}</ogc:Literal>"
        f"</ogc:PropertyIsLike>"
    )


def is_equal(property_name: str, value: Union[str, float]) -> str:
    """Constructs an OGC Filter for an attribute that is equal to
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (Union[str, float]): Value used in filter for comparison

    Returns:
        str: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsEqualTo", value)


def is_not_equal(property_name: str, value: Union[str, float]) -> str:
    """Constructs an OGC Filter for an attribute that is not equal to
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (Union[str, float]): Value used in filter for comparison

    Returns:
        str: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsNotEqualTo", value)


def is_less_than(property_name: str, value: float) -> str:
    """Constructs an OGC Filter for a numerical attribute that is less than
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        str: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsLessThan", value)


def is_greater_than(property_name: str, value: float) -> str:
    """Constructs an OGC Filter for a numerical attribute that is greater than
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        str: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsGreaterThan", value)


def is_less_than_or_equal_to(property_name: str, value: float) -> str:
    """Constructs an OGC Filter for a numerical attribute that is less
    than or equal to the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        str: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsLessThanOrEqualTo", value)


def is_greater_than_or_equal_to(property_name: str, value: float) -> str:
    """Constructs an OGC Filter for a numerical attribute that is greater
    than or equal to the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        str: A valid OGC XML filter
    """
    return single_attribute_filter(
        property_name, "PropertyIsGreaterThanOrEqualTo", value
    )
