"""Tests for the async NGD API client."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

import osdatahub
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


class TestAsyncHTTPClientProxy:
    """Tests for AsyncHTTPClient proxy support."""

    def test_get_proxy_https(self):
        """Test that HTTPS URLs use the https proxy."""
        client = AsyncHTTPClient(proxies={"https": "http://proxy:8080"})
        assert client._get_proxy("https://example.com") == "http://proxy:8080"

    def test_get_proxy_http(self):
        """Test that HTTP URLs use the http proxy."""
        client = AsyncHTTPClient(proxies={"http": "http://proxy:8080"})
        assert client._get_proxy("http://example.com") == "http://proxy:8080"

    def test_get_proxy_empty(self):
        """Test that empty proxies dict returns None."""
        client = AsyncHTTPClient(proxies={})
        assert client._get_proxy("https://example.com") is None

    def test_get_proxy_none(self):
        """Test that no proxies parameter returns None."""
        client = AsyncHTTPClient()
        assert client._get_proxy("https://example.com") is None

    def test_get_proxy_both(self):
        """Test proxy selection with both http and https configured."""
        client = AsyncHTTPClient(
            proxies={
                "http": "http://http-proxy:8080",
                "https": "http://https-proxy:8080",
            }
        )
        assert client._get_proxy("https://example.com") == "http://https-proxy:8080"
        assert client._get_proxy("http://example.com") == "http://http-proxy:8080"


class TestAsyncNGDProxy:
    """Tests for AsyncNGD proxy configuration."""

    def test_async_ngd_uses_proxies(self):
        """Test that AsyncNGD passes proxies to the HTTP client."""
        test_proxies = {"https": "http://proxy:8080"}

        with patch.object(osdatahub, "get_proxies", return_value=test_proxies):
            ngd = AsyncNGD("test-key", "test-collection")
            client = ngd._get_client()
            assert client._proxies == test_proxies

    def test_async_ngd_empty_proxies(self):
        """Test that AsyncNGD works with empty proxies (default)."""
        with patch.object(osdatahub, "get_proxies", return_value={}):
            ngd = AsyncNGD("test-key", "test-collection")
            client = ngd._get_client()
            assert client._proxies == {}

    @pytest.mark.asyncio
    async def test_async_ngd_get_collections_uses_proxies(self):
        """Test that get_collections passes proxies to the HTTP client."""
        test_proxies = {"https": "http://proxy:8080"}

        AsyncNGD.clear_collections_cache()

        with patch.object(osdatahub, "get_proxies", return_value=test_proxies):
            with patch.object(
                AsyncHTTPClient, "get", new_callable=AsyncMock
            ) as mock_get:
                with patch.object(AsyncHTTPClient, "close", new_callable=AsyncMock):
                    mock_get.return_value = {"collections": []}
                    await AsyncNGD.get_collections()

        AsyncNGD.clear_collections_cache()

    @pytest.mark.asyncio
    async def test_proxy_passed_to_aiohttp(self):
        """Test that proxy is actually passed to aiohttp session.get()."""
        test_proxies = {"https": "http://proxy:8080"}

        with patch.object(osdatahub, "get_proxies", return_value=test_proxies):
            with patch("aiohttp.ClientSession.get") as mock_session_get:
                mock_response = AsyncMock()
                mock_response.json = AsyncMock(
                    return_value={"features": [], "numberReturned": 0, "links": []}
                )
                mock_response.raise_for_status = MagicMock()
                mock_response.headers = {}
                mock_session_get.return_value.__aenter__.return_value = mock_response

                async with AsyncNGD("key", "collection", request_delay=0) as ngd:
                    await ngd.query(max_results=10)

                mock_session_get.assert_called()
                call_kwargs = mock_session_get.call_args.kwargs
                assert call_kwargs.get("proxy") == "http://proxy:8080"
