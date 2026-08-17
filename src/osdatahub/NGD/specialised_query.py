import logging
import re
from typing import Any, Dict, List, Union

import requests
from typeguard import typechecked
from typing_extensions import Match, Pattern

from osdatahub.NGD.models import AuthorityID, HighwayDedicationMatch
from osdatahub.NGD.ngd_api import NGD

_NETWORK_REFERENCE_KEY = "highwaydedicationnetworkreference"

# networkfeaturetype value
_ROAD_LINK = "Road Link"
_PATH_LINK = "Path Link"
_STREET = "Street"

# Highway Dedication authority ids should look like this ``esu4525_4348080549878_8``.
# Something like this should fail ``ess4525_4348080549878_8``.
_AUTHORITY_ID_PATTERN: Pattern[str] = re.compile(
    r"^(?P<prefix>esu)(?P<authority_code>\d{4})"
    r"_(?P<esu_id>[A-Za-z0-9]+)"
    r"_(?P<dedication_code>[A-Za-z0-9]+)$"
)

# The Road Link classification attributes indexed by OSID on a HighwayDedicationMatch
_CLASSIFICATION_FIELDS = ("roadclassification", "roadclassificationnumber")

# The dedication boolean attributes copied into a HighwayDedicationMatch
_DEDICATION_FLAGS = (
    "publicrightofway",
    "nationalcycleroute",
    "quietroute",
    "obstruction",
    "planningorder",
    "worksprohibited",
)


def _parse_authority_id(authority_id: str) -> AuthorityID:
    """
    Splits a Highway Dedication authority id into its component parts

    Args:
        authority_id (str): A full authority id in the form
            ``esu<authority_code>_<esu_id>_<dedication_code>``,
            e.g. ``esu4525_4348080549878_8``

    Returns:
        AuthorityID: The identifier

    Raises:
        ValueError: If the identifier does not match the expected format. The
            trailing dedication code is required: the OS NGD API only supports
            exact matches on ``authorityid``.

    Example::

        from osdatahub.NGD.specialised_query import _parse_authority_id

        parsed = _parse_authority_id("esu4525_4348080549878_8")
        parsed.authority_code  # "4525"
        parsed.esu_id          # "4348080549878"
    """
    match: Match[str] | None = _AUTHORITY_ID_PATTERN.match(authority_id.strip())
    if not match:
        raise ValueError(
            f"Invalid Highway Dedication authority id: {authority_id!r}. Expected the "
            "form 'esu<authority_code>_<esu_id>_<dedication_code>', e.g. "
            "'esu4525_4348080549878_8'."
        )

    return AuthorityID(raw=authority_id.strip(), **match.groupdict())


def _extract_network_references(feature: dict) -> Dict[str, List[str]]:
    """
    Collects the network references of a Highway Dedication feature by feature type.

    A dedication references the Streets, Road Links and Path Links it applies to
    through a nested ``highwaydedicationnetworkreference`` array.

    Those references are not filterable through the OS API, so you have to collect them
    to then filter them afterwards.

    This just iterates over that array and returns them.

    Args:
        feature (dict): A Highway Dedication GeoJSON Feature

    Returns:
        Dict[str, List[str]]: Identifiers keyed by ``networkfeaturetype``, e.g.
            ``{"Road Link": [...], "Street": [...]}``. Order is preserved and
            duplicates are removed. Feature types absent from the dedication are
            absent from the result.
    """
    references: Dict[str, List[str]] = {}

    for reference in (feature.get("properties") or {}).get(
        _NETWORK_REFERENCE_KEY
    ) or []:
        feature_type = reference.get("networkfeaturetype")
        reference_id = reference.get("networkreferenceid")

        if not feature_type or not reference_id:
            continue

        ids = references.setdefault(feature_type, [])
        if reference_id not in ids:
            ids.append(reference_id)

    return references


def _classifications_by_osid(roadlinks: List[dict]) -> Dict[str, Dict[str, Any]]:
    """
    Gets the road classification of each Road Link by its OSID.

    Args:
        roadlinks (List[dict]): Road Link GeoJSON Features

    Returns:
        Dict[str, Dict[str, Any]]: ``roadclassification`` and
            ``roadclassificationnumber`` keyed by OSID, e.g.
            ``{"71dfa822-…": {"roadclassification": "Unclassified",
            "roadclassificationnumber": None}}``
    """
    classifications: Dict[str, Dict[str, Any]] = {}

    for roadlink in roadlinks:
        properties = roadlink.get("properties") or {}
        osid = properties.get("osid") or roadlink.get("id")

        if osid:
            classifications[osid] = {
                field_name: properties.get(field_name)
                for field_name in _CLASSIFICATION_FIELDS
            }

    return classifications


def _strip_geometry(feature: dict) -> dict:
    """
    Returns the feature without its geometry attributes.

    Args:
        feature (dict): A GeoJSON Feature

    Returns:
        dict: The same Feature minus ``geometry`` and ``links``. ``properties`` is
            shared with the original rather than copied - it is never mutated.
    """
    return {k: v for k, v in feature.items() if k not in ("geometry", "links")}


class SpecialisedQuery:
    """
    Pre-built queries that implement more specialised join logic related OS NGD collections.

    Args:
        key (str): A valid OS Data Hub API key.
        highway_dedication_collection (str, optional): Overrides the Highway Dedication
            collection id. Defaults to ``trn-rami-highwaydedication-1``
        roadlink_collection (str, optional): Overrides the Road Link collection id.
            Defaults to ``trn-ntwk-roadlink-5``

    Example::

        from osdatahub import SpecialisedQuery
        from os import environ

        sq = SpecialisedQuery(environ.get("OS_API_KEY"))
        match = sq.roadlinks_by_authority_id("esu4525_4348080549878_8")

        match.esu_id          # "4348080549878"
        match.roadlink_osids  # the Road Links this ESU covers
        match.roadlinks       # their full GeoJSON features
    """

    HIGHWAY_DEDICATION_COLLECTION = "trn-rami-highwaydedication-1"
    ROADLINK_COLLECTION = "trn-ntwk-roadlink-5"

    def __init__(
        self,
        key: str,
        highway_dedication_collection: Union[str, None] = None,
        roadlink_collection: Union[str, None] = None,
    ):
        self.key: str = key
        # Use normal NGD client for synchronous calls
        self.highway_dedications: NGD = NGD(
            key, highway_dedication_collection or self.HIGHWAY_DEDICATION_COLLECTION
        )
        self.roadlinks: NGD = NGD(key, roadlink_collection or self.ROADLINK_COLLECTION)

    @typechecked
    def roadlinks_by_authority_id(
        self,
        authority_id: str,
        crs: Union[str, int, None] = None,
        include_roadlinks: bool = True,
        include_geometry: bool = False,
    ) -> Union[HighwayDedicationMatch, None]:
        """
        Finds the Road Links linked to a given AuthorityId (ESU IDs).

        Highway Dedications are keyed by a local-authority identifier of the form
        ``esu<authority_code>_<esu_id>_<dedication_code>``. Each dedication
        references the network features it applies to, so one authority id commonly
        resolves to several Road Links.

        Flag added to make returning the geometry optional as they can be quite large.

        Args:
            authority_id (str): A full Highway Dedication authority id, e.g.
                ``esu4525_4348080549878_8``. The trailing dedication code is
                required - see :func:`_parse_authority_id`
            crs (str|int, optional): The CRS for the returned Road Link geometries,
                either in the format "epsg:xxxx" or an epsg number. e.g. British
                National Grid can be supplied as "epsg:27700" or 27700.
                Available CRS values are: EPSG:27700, EPSG:4326, EPSG:7405,
                EPSG:3857, and CRS84. Defaults to CRS84. Only takes effect when
                ``include_geometry`` is True
            include_roadlinks (bool, optional): Whether to retrieve the full Road Link
                features. Set to False to make a single request and return only the
                Road Link OSIDs. Defaults to True.
            include_geometry (bool, optional): Whether to keep the ``geometry`` and
                ``links`` blocks on the returned features. This query is about
                attributes rather than linework, and the coordinate arrays dwarf
                everything else, so they are dropped by default. Defaults to False

        Returns:
            HighwayDedicationMatch: The dedication joined to its Road Links, or None
                if no dedication carries that authority id. Dedications covering only
                Path Links have an empty ``roadlink_osids``. Features in ``roadlinks``
                and ``dedication`` carry no geometry unless ``include_geometry`` is set.
                ``roadlink_classifications`` indexes each Road Link's classification by
                OSID, and is empty when ``include_roadlinks`` is False

        Raises:
            ValueError: If the authority id is malformed
            requests.exceptions.HTTPError: If the Highway Dedication query fails, or
                if a Road Link fetch fails with anything other than a 404. A Road Link
                missing from the collection is skipped with a warning; any other error,
                including a rate limit, is raised immediately.

        Example::

            from osdatahub import SpecialisedQuery
            from os import environ

            sq = SpecialisedQuery(environ.get("OS_API_KEY"))
            match = sq.roadlinks_by_authority_id("esu4525_4348080549878_8")

            for roadlink in match.roadlinks:
                print(roadlink["properties"]["roadclassification"])
        """
        parsed: AuthorityID = _parse_authority_id(authority_id)

        if crs and not include_geometry:
            logging.warning(
                "crs=%s has no effect because include_geometry is False - no geometry "
                "is returned to reproject",
                crs,
            )

        # authorityid is the only filterable parametre into this collection
        # Needs to be an exact match
        escaped = parsed.raw.replace("'", "''")
        response = self.highway_dedications.query(
            cql_filter=f"authorityid='{escaped}'", max_results=100
        )

        features = response.get("features") or []
        if not features:
            return None

        if len(features) > 1:
            logging.warning(
                "Authority id %s matched %d Highway Dedications, using the first",
                parsed.raw,
                len(features),
            )

        dedication = features[0]
        properties = dedication.get("properties") or {}
        references = _extract_network_references(dedication)

        # Isolate the Roadlinks specifically here
        # so we can go fetch their attributes
        roadlink_osids = references.get(_ROAD_LINK, [])
        roadlinks = (
            self._get_roadlinks(roadlink_osids, crs, include_geometry)
            if include_roadlinks
            else []
        )

        return HighwayDedicationMatch(
            authority_id=parsed,
            description=properties.get("description"),
            usrns=references.get(_STREET, []),
            roadlink_osids=roadlink_osids,
            pathlink_ids=references.get(_PATH_LINK, []),
            roadlinks=roadlinks,
            roadlink_classifications=_classifications_by_osid(roadlinks),
            dedication=dedication if include_geometry else _strip_geometry(dedication),
            **{flag: properties.get(flag) for flag in _DEDICATION_FLAGS},
        )

    def _get_roadlinks(
        self,
        osids: List[str],
        crs: Union[str, int, None] = None,
        include_geometry: bool = False,
    ) -> List[dict]:
        """
        Retrieves Road Link features by OSID, skipping any that can't be retrieved.

        Include geometry defaults to False for now.

        Args:
            osids (List[str]): Road Link OSIDs
            crs (str|int, optional): The CRS for the returned geometries
            include_geometry (bool, optional): Whether to keep the ``geometry`` and
                ``links`` blocks on each feature. Defaults to False

        Returns:
            List[dict]: The Road Link GeoJSON Features that were found

        Raises:
            requests.exceptions.HTTPError: For anything other than a 404. A missing
                feature is skipped, but a rate limit or server fault would silently
                truncate the results, so it is surfaced instead
        """
        roadlinks = []

        for osid in osids:
            try:
                feature = self.roadlinks.query_feature(osid, crs=crs)
            except requests.exceptions.HTTPError as e:
                if e.response is None or e.response.status_code != 404:
                    raise

                logging.warning(
                    "Road Link %s is not in %s, skipping",
                    osid,
                    self.roadlinks.collection,
                )
                continue

            roadlinks.append(feature if include_geometry else _strip_geometry(feature))

        return roadlinks
