import asyncio
import time


class RateLimiter:
    """
    This class provides two levels of rate limiting:

    1. Concurrent request limiting via asyncio.Semaphore
    2. Time-based delay between requests to prevent burst traffic

    Args:
        max_concurrent: Maximum number of concurrent requests (default: 5)
        request_delay: Minimum delay in seconds between requests (default: 0.02)

    Example::

        limiter = RateLimiter(max_concurrent=5, request_delay=0.3)
        async with limiter:
            await make_request()
    """

    def __init__(self, max_concurrent: int = 5, request_delay: float = 0.02) -> None:
        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(max_concurrent)
        self._request_delay: float = request_delay
        self._last_request_time: float = 0.0
        self._lock: asyncio.Lock = asyncio.Lock()

    async def __aenter__(self) -> "RateLimiter":
        """Acquire semaphore and enforce delay between requests."""
        await self._semaphore.acquire()
        await self._enforce_delay()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Release the semaphore."""
        self._semaphore.release()

    async def _enforce_delay(self) -> None:
        """Ensure minimum delay between requests."""
        async with self._lock:
            now = time.monotonic()
            elapsed = now - self._last_request_time
            if elapsed < self._request_delay:
                await asyncio.sleep(self._request_delay - elapsed)
            self._last_request_time = time.monotonic()

    @property
    def max_concurrent(self) -> int:
        """Return the maximum number of concurrent requests allowed."""
        return self._semaphore._value

    @property
    def request_delay(self) -> float:
        """Return the minimum delay between requests."""
        return self._request_delay
