import requests


def check_length(func):
    def wrapper(*args, **kwargs):
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
    return requests.get(*args, **kwargs)
 
 
@check_length
def post(*args, **kwargs):
    return requests.post(*args, **kwargs)