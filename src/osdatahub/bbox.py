from dataclasses import astuple, dataclass


@dataclass
class BBox:
    """
    BBox is a dataclass that specifies a rectangular polygon made up of north, south, east and west. It is indiscriminate
    of CRS and so is used as part of the more comprehensive Extent class
    """

    west: float
    south: float
    east: float
    north: float

    def __iter__(self):
        return (c for c in astuple(self))

    def __getitem__(self, index):
        return list(self)[index]

    def to_string(self, precision: int = None) -> str:
        """
        Converts bounding box into string

        Args:
            precision (int): Decimal point rounding precision. Defaults to None (no rounding)

        Returns:
            str: bounding box in string form
        """
        return ",".join(str(round(c, precision) if precision is not None else c) for c in self)
