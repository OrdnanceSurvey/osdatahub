import json

from requests.exceptions import HTTPError


RESPONSE_CODES = {
    200: ("OK", "Request has been successful."),
    304: (
        "Not Modified",
        "In response to a conditional GET request this response indicates that the underlying data has not changed since the previous request, and cached results may be re-used.",
    ),
    400: ("Bad request", "E.g. missing query parameter, malformed syntax."),
    401: (
        "Unauthorized",
        "API key is either incorrect, or does not permit access to the chosen product",
    ),
    403: (
        "Forbidden",
        "The client has authenticated its access but does not have sufficient rights to complete the request.",
    ),
    404: ("Not found", "The server has not found anything matching the Request-URI."),
    405: (
        "Method not allowed",
        "Request used an unsupported HTTP method, e.g. DELETE or PUT.",
    ),
    429: (
        "Too many requests",
        "Exceeded the number of requests per minute (rate-limit).",
    ),
    500: ("Internal server error", "Generic internal server error."),
    503: ("Service unavailable", "Temporary outage due to overloading or maintenance."),
}


def raise_http_error(response):
    code = response.status_code
    if code in RESPONSE_CODES:
        info = RESPONSE_CODES[code]
        url = response.url
        error_str = f"Unsuccessful query: {url}\n\nError {code} - {info[0]}: {info[1]}"
    else:
        try:
            is_too_large = response.json()["fault"]["detail"]["errorcode"] == "protocol.http.TooBigLine"
        except (KeyError, json.decoder.JSONDecodeError):
            is_too_large = False

        if is_too_large:
            error_str = "Query is too large. Please try simplifying it (e.g. reducing the vertices of a polygon)."
        else:
            error_str = response.text
    raise HTTPError(error_str)
