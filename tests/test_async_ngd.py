"""Tests for the async NGD API client."""

import os
from unittest.mock import AsyncMock, patch

import pytest

from osdatahub import Extent
from osdatahub.AsyncAPI import AsyncHTTPClient
from osdatahub.NGD.async_ngd_api import AsyncNGD

API_KEY = os.environ.get("OS_API_KEY")


@pytest.mark.asyncio
async def test_async_ngd_query():
    """Test basic async NGD query functionality."""
    response = {
        "type": "FeatureCollection",
        "features": [{"id": 1}, {"id": 2}],
        "numberReturned": 2,
        "links": [],
    }

    with patch.object(AsyncHTTPClient, "get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = response

        async with AsyncNGD("test-key", "test-collection", request_delay=0) as ngd:
            result = await ngd.query(max_results=10)

        assert result.numberReturned == 2
        assert len(result.features) == 2


@pytest.mark.asyncio
@pytest.mark.skipif(not API_KEY, reason="Test API key not available")
@pytest.mark.parametrize(
    "collection",
    [
        "trn-ntwk-roadlink-4",
        "trn-ntwk-street-1",
    ],
)
async def test_async_ngd_query_real_data(collection):
    """Test async NGD query with real API."""
    assert API_KEY is not None
    extent = Extent.from_bbox((436000, 114000, 438000, 116000), "EPSG:27700")

    async with AsyncNGD(
        key=API_KEY,
        collection=collection,
        max_concurrent=5,
        request_delay=0.02,
    ) as ngd:
        result = await ngd.query(extent=extent, max_results=None)

    assert result.numberReturned > 0
    assert len(result.features) == result.numberReturned
