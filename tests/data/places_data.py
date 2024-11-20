from pytest import param
from typeguard import TypeCheckError

def test_format_fq():
    test_variables = "classification_codes, logical_states, expected_result"
    test_data = [
        param("ABC", None, ["classification_code:ABC"]),
        param(
            ("ABC", "DEF"), None, ["classification_code:ABC classification_code:DEF"]
        ),
        param(
            ["ABC", "DEF"], None, ["classification_code:ABC classification_code:DEF"]
        ),
        param((), None, []),
        param(None, "5", ["logical_status_code:5"]),
        param(None, 5, ["logical_status_code:5"]),
        param("ABC", "5", ["classification_code:ABC", "logical_status_code:5"]),
        param(
            ("ABC", "DEF"),
            5,
            [
                "classification_code:ABC classification_code:DEF",
                "logical_status_code:5",
            ],
        ),
    ]
    return test_variables, test_data


def test_format_fq_errors():
    test_variables = "classification_codes, logical_states, expected_result"
    test_data = [
        param(1, None, (TypeError, TypeCheckError)),
        param(None, "ABC", (TypeError, TypeCheckError)),
        param(None, ("1", "2"), (TypeError, TypeCheckError)),
    ]
    return test_variables, test_data
