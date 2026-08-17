from os import environ
from unittest import mock

import pytest
from dotenv import load_dotenv

from osdatahub.NGD.specialised_query import SpecialisedQuery
from tests.data import specialised_query_data as sq_data

load_dotenv()

API_KEY = environ.get("OSDATAHUB_TEST_KEY")


class TestRoadlinksByAuthorityID:
    @mock.patch("osdatahub.get")
    def test_specialised_query_api_call(self, request_mocked):
        request_mocked.side_effect = sq_data.mock_ngd_get

        match = SpecialisedQuery("API-KEY").roadlinks_by_authority_id(
            sq_data.AUTHORITY_ID
        )

        # authorityid is the only filterable route into the collection, so the exact
        # filter string matters.
        request_mocked.assert_any_call(
            sq_data.HIGHWAY_DEDICATION_ITEMS,
            params={
                "filter": f"authorityid='{sq_data.AUTHORITY_ID}'",
                "limit": 100,
                "offset": 0,
            },
            headers=mock.ANY,
            proxies={},
        )

        assert match.authority_code == "4525"
        assert match.esu_id == "4348080549878"
        assert match.authority_id.dedication_code == "8"
        assert match.description == "All Vehicles"
        assert match.publicrightofway is False

        # One authority id resolves to many Road Links
        assert match.roadlink_osids == sq_data.ROADLINK_OSIDS
        assert [r["id"] for r in match.roadlinks] == sq_data.ROADLINK_OSIDS
        assert match.usrns == sq_data.USRNS
        assert match.pathlink_ids == []
        assert match.roadlink_classifications == sq_data.CLASSIFICATIONS

    @mock.patch("osdatahub.get")
    def test_specialised_query_strips_geometry(self, request_mocked):
        request_mocked.side_effect = sq_data.mock_ngd_get
        sq = SpecialisedQuery("API-KEY")

        match = sq.roadlinks_by_authority_id(sq_data.AUTHORITY_ID)

        assert match.roadlinks[0]["properties"]["roadclassification"] == "Unclassified"
        assert "geometry" not in match.roadlinks[0]
        assert "links" not in match.roadlinks[0]
        assert "geometry" not in match.dedication
        assert match.dedication["properties"]["authorityid"] == sq_data.AUTHORITY_ID

        with_geometry = sq.roadlinks_by_authority_id(
            sq_data.AUTHORITY_ID, include_geometry=True
        )

        assert with_geometry.roadlinks[0]["geometry"]["type"] == "LineString"
        assert with_geometry.dedication is sq_data.DEDICATION

    @mock.patch("osdatahub.get")
    def test_specialised_query_without_roadlinks(self, request_mocked):
        request_mocked.side_effect = sq_data.mock_ngd_get

        match = SpecialisedQuery("API-KEY").roadlinks_by_authority_id(
            sq_data.AUTHORITY_ID, include_roadlinks=False
        )

        assert match.roadlink_osids == sq_data.ROADLINK_OSIDS
        assert match.roadlinks == []
        assert match.roadlink_classifications == {}
        assert request_mocked.call_count == 1


class TestRoadlinksByAuthorityIDLive:
    @pytest.mark.skipif(not API_KEY, reason="Test API key not available")
    def test_specialised_query_live(self):
        sq = SpecialisedQuery(API_KEY)

        match = sq.roadlinks_by_authority_id(sq_data.AUTHORITY_ID)

        assert match.authority_code == "4525"
        assert match.esu_id == "4348080549878"
        assert match.description == "All Vehicles"
        assert sorted(match.usrns) == sq_data.USRNS
        assert sorted(match.roadlink_osids) == sq_data.ROADLINK_OSIDS
        assert {r["properties"]["osid"] for r in match.roadlinks} == set(
            sq_data.ROADLINK_OSIDS
        )
        assert set(match.roadlink_classifications) == set(sq_data.ROADLINK_OSIDS)

        # Proves OS still returns geometry where we expect it, and that we strip it.
        assert all("geometry" not in r for r in match.roadlinks)
        assert "geometry" not in match.dedication

        with_geometry = sq.roadlinks_by_authority_id(
            sq_data.AUTHORITY_ID, crs=27700, include_geometry=True
        )

        assert with_geometry.roadlinks[0]["geometry"]["coordinates"]
        assert with_geometry.dedication["geometry"]["type"] == "LineString"

    @pytest.mark.skipif(not API_KEY, reason="Test API key not available")
    def test_specialised_query_live_unknown_authority_id(self):
        sq = SpecialisedQuery(API_KEY)

        assert sq.roadlinks_by_authority_id("esu4525_0000000000000_8") is None
