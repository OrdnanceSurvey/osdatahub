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
        if hasattr(SpatialFilterTypes, filter_type):
            return getattr(SpatialFilterTypes, filter_type)
        else:
            raise ValueError(f"unrecognised spatial filter type: {filter_type}")
