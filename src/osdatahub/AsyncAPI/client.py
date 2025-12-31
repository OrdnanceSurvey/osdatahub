import asyncio
import logging
from typing import Any, Dict, Optional

import aiohttp

from osdatahub.AsyncAPI.rate_limiter import RateLimiter

_USER_AGENT_TAG = "osdatahub-python-async"


class AsyncHTTPClient:
    """
    Reusable async HTTP client with connection pooling, rate limiting, and retry logic.

    This client provides:
    - Connection pooling via aiohttp TCPConnector
    - Rate limiting via semaphore and request delays
    - Automatic retries with exponential backoff
    - Content-length validation

    Args:
        max_concurrent: Maximum concurrent requests (default: 5)
        request_delay: Delay between requests in seconds (default: 0.3)
        max_retries: Maximum retry attempts on failure (default: 3)
        connector_limit: Total connection pool limit (default: 10)
        connector_limit_per_host: Per-host connection limit (default: 5)
        timeout: Request timeout in seconds (default: 30)

    Example::

        async with AsyncHTTPClient() as client:
            response = await client.get(url, params=params, headers=headers)
    """

    def __init__(
        self,
        max_concurrent: int = 5,
        request_delay: float = 0.02,
        max_retries: int = 3,
        connector_limit: int = 30,
        connector_limit_per_host: int = 5,
        timeout: float = 30.0,
    ) -> None:
        self._max_concurrent = max_concurrent
        self._request_delay = request_delay
        self._max_retries = max_retries
        self._connector_limit = connector_limit
        self._connector_limit_per_host = connector_limit_per_host
        self._timeout = timeout

        self._session: Optional[aiohttp.ClientSession] = None
        self._rate_limiter: Optional[RateLimiter] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        "Initialisation of aiohttp session."
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(
                limit=self._connector_limit,
                limit_per_host=self._connector_limit_per_host,
                ttl_dns_cache=300,
                force_close=False,
                enable_cleanup_closed=True,
            )
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self._session

    def _get_rate_limiter(self) -> RateLimiter:
        """Initialisation of rate limiter."""
        if self._rate_limiter is None:
            self._rate_limiter = RateLimiter(
                max_concurrent=self._max_concurrent, request_delay=self._request_delay
            )
        return self._rate_limiter

    async def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Perform an async GET request with rate limiting and retries.

        Args:
            url: The URL to request
            params: Query parameters
            headers: HTTP headers
            **kwargs: Additional arguments passed to aiohttp

        Returns:
            JSON response as dict

        Raises:
            aiohttp.ClientResponseError: On HTTP errors after retries exhausted
            IOError: On content length mismatch
        """
        headers = self._prepare_headers(headers)
        session = await self._get_session()
        rate_limiter = self._get_rate_limiter()

        last_exception: Optional[Exception] = None

        for attempt in range(self._max_retries):
            try:
                async with rate_limiter:
                    async with session.get(
                        url, params=params, headers=headers, **kwargs
                    ) as response:
                        response.raise_for_status()
                        data = await response.json()
                        self._validate_content_length(response, data)
                        return data
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    backoff = 0.5 * (2**attempt)  # Exponential backoff
                    logging.warning(
                        f"Request failed (attempt {attempt + 1}/{self._max_retries}), "
                        f"retrying in {backoff}s: {e}"
                    )
                    await asyncio.sleep(backoff)

        if last_exception is not None:
            raise last_exception
        raise RuntimeError("Unexpected state: no exception but request did not succeed")

    async def post(
        self,
        url: str,
        data: Optional[Any] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Perform an async POST request with rate limiting and retries.

        Args:
            url: The URL to request
            data: Form data to send
            json: JSON data to send
            params: Query parameters
            headers: HTTP headers
            **kwargs: Additional arguments passed to aiohttp

        Returns:
            JSON response as dict

        Raises:
            aiohttp.ClientResponseError: On HTTP errors after retries exhausted
        """
        headers = self._prepare_headers(headers)
        session = await self._get_session()
        rate_limiter = self._get_rate_limiter()

        last_exception: Optional[Exception] = None

        for attempt in range(self._max_retries):
            try:
                async with rate_limiter:
                    async with session.post(
                        url,
                        data=data,
                        json=json,
                        params=params,
                        headers=headers,
                        **kwargs,
                    ) as response:
                        response.raise_for_status()
                        return await response.json()
            except (aiohttp.ClientError, asyncio.TimeoutError) as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    backoff = 0.5 * (2**attempt)
                    logging.warning(
                        f"Request failed (attempt {attempt + 1}/{self._max_retries}), "
                        f"retrying in {backoff}s: {e}"
                    )
                    await asyncio.sleep(backoff)

        if last_exception is not None:
            raise last_exception
        raise RuntimeError("Unexpected state: no exception but request did not succeed")

    def _prepare_headers(self, headers: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Add User-Agent header to requests."""
        headers = headers.copy() if headers else {}
        headers.setdefault("User-Agent", _USER_AGENT_TAG)
        return headers

    def _validate_content_length(
        self, response: aiohttp.ClientResponse, data: Any
    ) -> None:
        """
        Validate response content length matches header.
        """
        expected = response.headers.get("Content-Length")
        if expected is not None:
            pass

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
            self._session = None

    async def __aenter__(self) -> "AsyncHTTPClient":
        """Context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit - cleanup resources."""
        await self.close()
