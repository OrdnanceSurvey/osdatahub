"""
This requests wrapper is included to handle incomplete responses from the api.
Information and inspiration from https://blog.petrzemek.net/2018/04/22/on-incomplete-http-reads-and-the-requests-library-in-python/
"""

import requests


def check_length(func):
    """
    Decorator function that checks if the response content length is as expected.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that performs the content length check.

        Returns:
            The response object if the content length check passes.

        Raises:
            IOError: If the content length check fails.
        """
        response = func(*args, **kwargs)

        expected_length = response.headers.get('Content-Length')

        if expected_length is None:
            return response

        actual_length = response.raw.tell()
        expected_length = int(expected_length)
        if actual_length < expected_length:
            deficit = expected_length - actual_length
            raise IOError(
                f'incomplete read ({actual_length} bytes read, {deficit} more expected)'
            )

        return response
    return wrapper


@check_length
def get(*args, **kwargs):
    """
    Sends a GET request to the specified URL.

    Args:
        *args: Positional arguments to be passed to the requests.get function.
        **kwargs: Keyword arguments to be passed to the requests.get function.

    Returns:
        The response object if the content length check passes.

    Raises:
        IOError: If the content length check fails.
    """
    return requests.get(*args, **kwargs)


@check_length
def post(*args, **kwargs):
    """
    Sends a POST request to the specified URL.

    Args:
        *args: Positional arguments to be passed to the requests.post function.
        **kwargs: Keyword arguments to be passed to the requests.post function.

    Returns:
        The response object if the content length check passes.

    Raises:
        IOError: If the content length check fails.
    """
    return requests.post(*args, **kwargs)
