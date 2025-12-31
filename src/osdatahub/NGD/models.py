from dataclasses import dataclass
from typing import Any, Dict, List, Optional

"""
Structured a bit like Rust does From and Into.
See here: https://doc.rust-lang.org/rust-by-example/conversion/from_into.html
"""


@dataclass
class FeatureCollection:
    """GeoJSON FeatureCollection response from NGD API."""

    type: str
    features: List[Dict[str, Any]]
    numberReturned: int
    links: List[Dict[str, Any]]
    timeStamp: Optional[str] = None
    numberMatched: Optional[int] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FeatureCollection":
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
