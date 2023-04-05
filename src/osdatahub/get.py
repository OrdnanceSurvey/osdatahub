import requests


def get(*args, **kwargs):
    response = requests.get(*args, **kwargs)
 
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
