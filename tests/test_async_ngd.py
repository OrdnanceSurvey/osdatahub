"""Tests for the async NGD API client."""

from unittest.mock import AsyncMock, patch

import pytest

from osdatahub.AsyncAPI import AsyncHTTPClient
from osdatahub.NGD.async_ngd_api import AsyncNGD


# TODO: Add full suite of tests
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
