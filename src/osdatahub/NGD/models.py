from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

"""
Structured a bit like Rust does From and Into.
See here: https://doc.rust-lang.org/rust-by-example/conversion/from_into.html
"""


@dataclass
class NGDFeatureCollection:
    """GeoJSON FeatureCollection response from NGD API."""

    type: str
    features: List[Dict[str, Any]]
    numberReturned: int
    links: List[Dict[str, Any]]
    timeStamp: Optional[str] = None
    numberMatched: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "NGDFeatureCollection":
        """Create FeatureCollection from API response dict."""
        return cls(
            type=data.get("type", "FeatureCollection"),
            features=data.get("features", []),
            numberReturned=data.get("numberReturned", 0),
            links=data.get("links", []),
            timeStamp=data.get("timeStamp"),
            numberMatched=data.get("numberMatched"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dict for GeoJSON compatibility."""
        result: Dict[str, Any] = {
            "type": self.type,
            "features": self.features,
            "numberReturned": self.numberReturned,
            "links": self.links,
        }
        if self.timeStamp is not None:
            result["timeStamp"] = self.timeStamp
        if self.numberMatched is not None:
            result["numberMatched"] = self.numberMatched
        return result


@dataclass(frozen=True)
class AuthorityID:
    """The seperate parts of a Highway Dedication's ``authorityid``.

    Highway Dedication features carry an  authority identifier in the form
    ``esu<authority_code>_<esu_id>_<dedication_code>``, for example
    ``esu4525_4348080549878_8``. The authority code matches the
    ``responsibleauthority_identifier`` of the Street/USRN the ESU belongs to.

    Attributes:
        raw (str): The unmodified authority id as returned by the API
        prefix (str): The non-numeric prefix, conventionally ``esu``
        authority_code (str): The local authority code, e.g. ``4525``
        esu_id (str): The Elementary Street Unit id
        dedication_code (str): The highway dedication code, e.g. ``8``
    """

    raw: str
    prefix: str
    authority_code: str
    esu_id: str
    dedication_code: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a plain dict."""
        return {
            "raw": self.raw,
            "prefix": self.prefix,
            "authority_code": self.authority_code,
            "esu_id": self.esu_id,
            "dedication_code": self.dedication_code,
        }


@dataclass
class HighwayDedicationMatch:
    """A Highway Dedication joined to it's corresponding Road Links .

    A single dedication commonly references several Road Links, so
    ``roadlink_osids`` is one-to-many.

    Dedications that only cover Path Links (footpaths) legitimately have no Road Links at all.

    Attributes:
        authority_id (AuthorityID): The ``authorityid``
        description (str, optional): The dedication type, e.g. ``All Vehicles``
        publicrightofway (bool, optional): Whether a public right of way exists
        nationalcycleroute (bool, optional): Whether part of the National Cycle Network
        quietroute (bool, optional): Whether designated a quiet route
        obstruction (bool, optional): Whether an obstruction is present
        planningorder (bool, optional): Whether subject to a planning order
        worksprohibited (bool, optional): Whether street works are prohibited
        usrns (List[str]): USRNs of the Streets the dedication references
        roadlink_osids (List[str]): OSIDs of the referenced Road Links
        pathlink_ids (List[str]): Identifiers of the referenced Path Links
        roadlinks (List[Dict]): The Road Link GeoJSON features, empty when they were
            not requested. Geometry is omitted unless ``include_geometry`` was set
        roadlink_classifications (Dict[str, Dict]): ``roadclassification`` and
            ``roadclassificationnumber`` keyed by Road Link OSID, saving a walk through
            ``roadlinks``. Empty when the Road Links were not requested
        dedication (Dict): The source Highway Dedication GeoJSON feature, likewise
            without geometry unless ``include_geometry`` was set
    """

    authority_id: "AuthorityID"
    description: Optional[str] = None
    publicrightofway: Optional[bool] = None
    nationalcycleroute: Optional[bool] = None
    quietroute: Optional[bool] = None
    obstruction: Optional[bool] = None
    planningorder: Optional[bool] = None
    worksprohibited: Optional[bool] = None
    usrns: List[str] = field(default_factory=list)
    roadlink_osids: List[str] = field(default_factory=list)
    pathlink_ids: List[str] = field(default_factory=list)
    roadlinks: List[Dict[str, Any]] = field(default_factory=list)
    roadlink_classifications: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    dedication: Dict[str, Any] = field(default_factory=dict)

    @property
    def esu_id(self) -> str:
        """The Elementary Street Unit id, e.g. ``4348080549878``."""
        return self.authority_id.esu_id

    @property
    def authority_code(self) -> str:
        """The local authority code, e.g. ``4525``."""
        return self.authority_id.authority_code

    def to_dict(self) -> Dict[str, Any]:
        """Convert to a plain, JSON-serialisable dict."""
        return {
            "authority_id": self.authority_id.to_dict(),
            "description": self.description,
            "publicrightofway": self.publicrightofway,
            "nationalcycleroute": self.nationalcycleroute,
            "quietroute": self.quietroute,
            "obstruction": self.obstruction,
            "planningorder": self.planningorder,
            "worksprohibited": self.worksprohibited,
            "usrns": self.usrns,
            "roadlink_osids": self.roadlink_osids,
            "pathlink_ids": self.pathlink_ids,
            "roadlinks": self.roadlinks,
            "roadlink_classifications": self.roadlink_classifications,
            "dedication": self.dedication,
        }
