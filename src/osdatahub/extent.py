from dataclasses import dataclass
from typing import Collection, Union, Iterable

import osdatahub
from osdatahub.bbox import BBox
from osdatahub.ons_api import get_ons_geom
from shapely.geometry import Polygon, box
from shapely.geometry.point import Point

_VALID_CRS = ("EPSG:27700", "EPSG:3857", "EPSG:4326", "EPSG:7405", "CRS84")


@dataclass(frozen=True)
class Extent:
    """
    Extent is a dataclass that has two main uses:

        - It is a standardised way to store polygon extents that will interface
          with all of the osdatahub APIs.
        - It has multiple constructors that allow the user to create custom
          Extents without needing to write out polygon coordinates.

    """

    polygon: Polygon
    crs: str

    def __post_init__(self):
        if not isinstance(self.polygon, Polygon):
            raise TypeError("Extent expects geometry as a shapley Polygon")
        if self.crs.upper() not in _VALID_CRS:
            raise ValueError(
                f"Extent CRS must be one of {_VALID_CRS}, got '{self.crs}'"
            )

    @property
    def bbox(self) -> BBox:
        return BBox(*self.polygon.bounds)

    @property
    def xml_coords(self) -> str:
        coords = self.polygon.exterior.coords
        if self.crs.upper() == "EPSG:4326":
            return " ".join([f"{c2},{c1}" for c1, c2 in coords])
        return " ".join([f"{c1},{c2}" for c1, c2 in coords])

    @classmethod
    def from_bbox(cls, bbox: Union[Collection[float], BBox], crs: str) -> "Extent":
        """Creates a rectangular extent, given a bounding box.

        Args:
            bbox (Union[Collection[float], BBox]): A bounding box, passed in as either a
                BBox object or a collection of the form (west, south, east, north).
            crs (str): The CRS corresponding to the bouding box, must be either
                ''EPSG:4326', EPSG:27700' or 'EPSG:3857'.

        Raises:
            TypeError: If bbox is not a tuple or BBox object.

        Returns:
            Extent: A rectangular extent that matches
            the specified bounding box.
        """
        try:
            return Extent(box(*bbox), crs)
        except TypeError:
            raise TypeError(
                "bbox must be a BBox object or a collection "
                "of the form (west, south, east, north)"
            ) from None

    @classmethod
    def from_radius(cls, centre: Iterable, radius: float, crs: str) -> "Extent":
        """Creates a circular extent, given a centre point and a radius.

        Args:
            centre (Iterable): Either a coordinate tuple in the form (x, y)
                or a shapely Point.
            radius (float): The radius of the circle in metres
            crs (str): The CRS corresponding to the point coordinate,
                must be either 'EPSG:27700' or 'EPSG:3857'.

        Raises:
            TypeError: If centre is not a tuple or shapely Point.

        Returns:
            Extent: A rectangular extent that matches
            the specified bounding box.
        """
        if crs.upper() not in ("EPSG:27700", "EPSG:3857"):
            raise ValueError(
                f"crs must be one of ('EPSG:27700', 'EPSG:3857'), got {crs}"
            )
        if isinstance(centre, Iterable) and len(centre) == 2:
            return Extent(Point(*centre).buffer(radius), crs)
        elif isinstance(centre, Point):
            return Extent(centre.buffer(radius), crs)
        else:
            raise TypeError(
                "centre must be a shapely Point object "
                "or a coordinate tuple of the form (x, y)"
            )

    def set_crs(self, crs: str) -> "Extent":
        """
        Changes the coordinate reference system of the Extent object to the value specified

        Args:
            crs (str): The CRS to change to, must be either ‘’EPSG:4326’, EPSG:27700’ or ‘EPSG:3857’.

        Returns:
            Extent: A rectangular extent with an updated CRS
        """
        return Extent(self.polygon, crs)

    def is_within(self, bbox: Union[Collection[float], BBox]) -> bool:
        """
        Checks whether a bounding box is within the Extent object

        Args:
            bbox (Union[Collection[float], BBox]): A bounding box, passed in as either a
                BBox object or a collection of the form (west, south, east, north).

        Returns:
            bool: True if the bounding box is within the Extent object, False if not
        """
        try:
            bbox = BBox(*bbox)
        except TypeError:
            raise TypeError(
                "bbox must be a BBox object or a collection "
                "of the form (west, south, east, north)"
            ) from None
        return bbox[:2] <= self.bbox[:2] and bbox[-2:] >= self.bbox[-2:]

    def to_json(self):
        """
        Converts the extent object into a json

        Returns:
            dict: A json containing the coordinates of the Extent
        """
        coords = list(self.polygon.exterior.coords)
        if self.crs.upper() == "EPSG:4326":
            coords = [(c2, c1) for c1, c2 in coords]
        return {"type": "Polygon", "coordinates": [coords]}

    @classmethod
    def from_ons_code(cls, ons_code: str) -> "Extent":
        """Creates an extent of an existing ONS boundary.
        Note that the output will be in the "EPSG:4326" coordinate system.
        A full list of available ONS geographies can be found here:
        http://statistics.data.gov.uk/atlas/resource?uri=http://statistics.data.gov.uk/id/statistical-geography/K02000001

        Args:
            ons_code (str): The code for the desired geography
        Raises:
            ValueError: If the ONS geography is not a Polygon.

        Returns:
            Extent: An extent of the ONS geography.
        """
        geom = get_ons_geom(ons_code)
        geom_type = geom["type"]
        if geom_type != "Polygon":
            raise ValueError(
                f"osdatahub doesn't currently support geometry types other than Polygon. \n The ONS geography {ons_code} is a {geom_type}"
            )
        polygon = Polygon(geom["coordinates"][0])
        return Extent(polygon, "EPSG:4326")

    def __repr__(self):
        coords = list(self.polygon.exterior.coords)
        return (
            f"{self.__class__.__name__}(polygon=Polygon({coords})," f"crs='{self.crs}')"
        )

    def __eq__(self, o: object) -> bool:
        return self.polygon.equals(o.polygon) and (self.crs == o.crs)
