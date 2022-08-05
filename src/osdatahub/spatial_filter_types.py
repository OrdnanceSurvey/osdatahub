from typing import Callable

from osdatahub.filters import (contains, crosses, disjoint, equals, intersects,
                               overlaps, touches, within)


class SpatialFilterTypes:
    contains = contains
    crosses = crosses
    disjoint = disjoint
    equals = equals
    intersects = intersects
    overlaps = overlaps
    touches = touches
    within = within

    @classmethod
    def get(cls, filter_type: str) -> Callable:
        """
        Get relevant spatial filter from string
        
        Args:
        filter_type (str): name of ogc gml filter

        Returns:
            Callable: A function that generates the desired geospatial XML filter
        """
        if hasattr(SpatialFilterTypes, filter_type):
            return getattr(SpatialFilterTypes, filter_type)
        else:
            raise ValueError(f"unrecognised spatial filter type: {filter_type}")
