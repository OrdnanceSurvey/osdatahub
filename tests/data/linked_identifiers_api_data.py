from pytest import param


def test_get_endpoint():
    test_variables = "key, identifier, feature_type, identifier_type, expected_result"
    test_data = [
        param(
            "KEY",
            "IDENTIFIER",
            None,
            "TOID",
            "https://api.os.uk/search/links/v1/identifierTypes/TOID/IDENTIFIER?key=KEY",
            id="identifier_type only",
        ),
        param(
            "KEY",
            "IDENTIFIER",
            "Road",
            None,
            "https://api.os.uk/search/links/v1/featureTypes/Road/IDENTIFIER?key=KEY",
            id="feature_type only",
        ),
        param(
            "KEY",
            "IDENTIFIER",
            None,
            None,
            "https://api.os.uk/search/links/v1/identifiers/IDENTIFIER?key=KEY",
            id="no types",
        ),
    ]
    return test_variables, test_data
