import functools
import operator
from typing import Union

from osdatahub import Extent


def _binary_operator(*classes):
    def func_acceptor(func):
        def inner(instance, other):
            nonlocal classes
            classes = tuple(globals()[i] if isinstance(i, str) else i for i in classes)
            if not isinstance(other, classes):
                return NotImplemented
            return func(instance, other)

        return inner

    return func_acceptor


class Filter:
    """
    A container class for an OGD XML filter.
    Allows XML to be joined using `and` and `or` operations.
    It should not be instantiated directly, instead produced by one of the methods in this module.
    """

    def __init__(self, xml: str):
        self.xml: str = xml

    @staticmethod
    def _apply_op(filter1: str, filter2: str, operation: str) -> str:
        return f"<ogc:{operation}>{filter1}{filter2}</ogc:{operation}>"

    @_binary_operator("Filter", str)
    def __add__(self, other) -> "Filter":
        if isinstance(other, Filter):
            return Filter(self.xml + other.xml)
        return Filter(self.xml + other)

    @_binary_operator("Filter")
    def __and__(self, other) -> "Filter":
        return Filter(self._apply_op(self.xml, other.xml, "And"))

    def __bool__(self) -> bool:
        raise NotImplementedError("Did you use a boolean operation, meaning to use a bitwise operation instead?")

    def __eq__(self, other) -> bool:
        if isinstance(other, Filter):
            return self.xml == other.xml
        elif isinstance(other, str):
            return self.xml == other
        return False

    @_binary_operator("Filter", str)
    def __iadd__(self, other) -> "Filter":
        if isinstance(other, Filter):
            self.xml = self.xml + other.xml
        else:
            self.xml = self.xml + other
        return self

    @_binary_operator("Filter")
    def __iand__(self, other) -> "Filter":
        self.xml = self._apply_op(self.xml, other.xml, "And")
        return self

    @_binary_operator("Filter")
    def __ior__(self, other) -> "Filter":
        self.xml = self._apply_op(self.xml, other.xml, "Or")
        return self

    @_binary_operator("Filter")
    def __or__(self, other) -> "Filter":
        return Filter(self._apply_op(self.xml, other.xml, "Or"))

    @_binary_operator("Filter", str)
    def __radd__(self, other) -> "Filter":
        if isinstance(other, Filter):
            return Filter(other.xml + self.xml)
        return Filter(other + self.xml)

    @_binary_operator("Filter")
    def __rand__(self, other):
        return Filter(self._apply_op(other.xml, self.xml, "And"))

    def __repr__(self) -> str:
        return repr(self.xml)

    @_binary_operator("Filter")
    def __ror__(self, other):
        return Filter(self._apply_op(other.xml, self.xml, "Or"))

    def __str__(self) -> str:
        return self.xml


def filter_or(*filters: Filter) -> Filter:
    """Constructs an OGC XML filter that performs an 'or' on the given filters

    Args:
        filters (Filter): The filters to be joined

    Returns:
        Filter: A valid OGC XML filter
    """
    return functools.reduce(operator.or_, filters)


def filter_and(*filters: Filter) -> Filter:
    """Constructs an OGC XML filter that performs an 'and' on the given filters

    Args:
        filters (Filter): The filters to be joined

    Returns:
        Filter: A valid OGC XML filter
    """
    return functools.reduce(operator.and_, filters)


def spatial_filter(operator: str, extent: Extent) -> Filter:
    """Constructs an OGC XML filter using the given operator string and the given extent

    Args:
        operator (str): Case-sensitive name of operator for OGC filter string
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    coords = extent.xml_coords
    crs = extent.crs.upper()
    return Filter(
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


def intersects(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that intersects the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Intersects", extent)


def touches(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that touches the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Touches", extent)


def disjoint(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that does not interact with the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Disjoint", extent)


def contains(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that contains the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Contains", extent)


def within(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that is within the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Within", extent)


def crosses(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that crosses the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Crosses", extent)


def overlaps(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that overlaps the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Overlaps", extent)


def equals(extent: Extent) -> Filter:
    """Constructs an OGC XML filter for data that is equal to the given extent

    Args:
        extent (Extent): The desired region to be filtered, given as an Extent object

    Returns:
        Filter: A valid OGC XML filter
    """
    return spatial_filter("Equals", extent)


def single_attribute_filter(property_name, filter_name, value) -> Filter:
    return Filter(
        f"<ogc:{filter_name}>"
        f"<ogc:PropertyName>{property_name}</ogc:PropertyName>"
        f"<ogc:Literal>{value}</ogc:Literal>"
        f"</ogc:{filter_name}>"
    )


def is_between(property_name: str, lower: float, upper: float) -> Filter:
    """Constructs an OGC XML filter for a numerical attribute between 2 values

    Args:
        property_name (str): Property / attribute name to be filtered
        lower (float): The filter's lower bound
        upper (float): The filter's upper bound

    Returns:
        Filter: A valid OGC XML filter
    """
    return Filter(
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
) -> Filter:
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
        Filter: A valid OGC XML filter
    """
    return Filter(
        f'<ogc:PropertyIsLike wildCard="{wildcard}" singleChar="{single_char}" escapeChar="{escape_char}">'
        f"<ogc:ValueReference>{property_name}</ogc:ValueReference>"
        f"<ogc:Literal>{value}</ogc:Literal>"
        f"</ogc:PropertyIsLike>"
    )


def is_equal(property_name: str, value: Union[str, float]) -> Filter:
    """Constructs an OGC Filter for an attribute that is equal to
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (Union[str, float]): Value used in filter for comparison

    Returns:
        Filter: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsEqualTo", value)


def is_not_equal(property_name: str, value: Union[str, float]) -> Filter:
    """Constructs an OGC Filter for an attribute that is not equal to
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (Union[str, float]): Value used in filter for comparison

    Returns:
        Filter: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsNotEqualTo", value)


def is_less_than(property_name: str, value: float) -> Filter:
    """Constructs an OGC Filter for a numerical attribute that is less than
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        Filter: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsLessThan", value)


def is_greater_than(property_name: str, value: float) -> Filter:
    """Constructs an OGC Filter for a numerical attribute that is greater than
    the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        Filter: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsGreaterThan", value)


def is_less_than_or_equal_to(property_name: str, value: float) -> Filter:
    """Constructs an OGC Filter for a numerical attribute that is less
    than or equal to the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        Filter: A valid OGC XML filter
    """
    return single_attribute_filter(property_name, "PropertyIsLessThanOrEqualTo", value)


def is_greater_than_or_equal_to(property_name: str, value: float) -> Filter:
    """Constructs an OGC Filter for a numerical attribute that is greater
    than or equal to the input value

    Args:
        property_name (str): Property / attribute name to be filtered
        value (float): Value used in filter for comparison

    Returns:
        Filter: A valid OGC XML filter
    """
    return single_attribute_filter(
        property_name, "PropertyIsGreaterThanOrEqualTo", value
    )
