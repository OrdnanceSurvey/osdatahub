from pytest import param


def test_convert_address_to_feature():
    test_variables = "address, crs, expected_result"
    test_data = [
        param(
            {
                "UPRN": "10094212630",
                "UDPRN": "55819024",
                "ADDRESS": "UNIT D4, ADANAC PARK, ADANAC DRIVE, NURSLING, SOUTHAMPTON, SO16 0BT",
                "SUB_BUILDING_NAME": "UNIT D4",
                "BUILDING_NAME": "ADANAC PARK",
                "THOROUGHFARE_NAME": "ADANAC DRIVE",
                "DEPENDENT_LOCALITY": "NURSLING",
                "POST_TOWN": "SOUTHAMPTON",
                "POSTCODE": "SO16 0BT",
                "RPC": "2",
                "X_COORDINATE": 437230.0,
                "Y_COORDINATE": 115775.0,
                "LNG": -163806.07,
                "LAT": 6610726.44,
                "STATUS": "HISTORICAL",
                "LOGICAL_STATUS_CODE": "8",
                "CLASSIFICATION_CODE": "CI01",
                "CLASSIFICATION_CODE_DESCRIPTION": "Factory/Manufacturing",
                "LOCAL_CUSTODIAN_CODE": 1760,
                "LOCAL_CUSTODIAN_CODE_DESCRIPTION": "TEST VALLEY",
                "POSTAL_ADDRESS_CODE": "D",
                "POSTAL_ADDRESS_CODE_DESCRIPTION": "A record which is linked to PAF",
                "BLPU_STATE_CODE": "null",
                "BLPU_STATE_CODE_DESCRIPTION": "Unknown/Not applicable",
                "TOPOGRAPHY_LAYER_TOID": "osgb5000005278503035",
                "PARENT_UPRN": "10094212626",
                "LAST_UPDATE_DATE": "01/09/2021",
                "ENTRY_DATE": "20/08/2019",
                "LANGUAGE": "EN",
                "MATCH": 0.4,
                "MATCH_DESCRIPTION": "NO MATCH",
            },
            "epsg:3857",
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [-163806.07, 6610726.44]},
                "properties": {
                    "UPRN": "10094212630",
                    "UDPRN": "55819024",
                    "ADDRESS": "UNIT D4, ADANAC PARK, ADANAC DRIVE, NURSLING, SOUTHAMPTON, SO16 0BT",
                    "SUB_BUILDING_NAME": "UNIT D4",
                    "BUILDING_NAME": "ADANAC PARK",
                    "THOROUGHFARE_NAME": "ADANAC DRIVE",
                    "DEPENDENT_LOCALITY": "NURSLING",
                    "POST_TOWN": "SOUTHAMPTON",
                    "POSTCODE": "SO16 0BT",
                    "RPC": "2",
                    "X_COORDINATE": 437230.0,
                    "Y_COORDINATE": 115775.0,
                    "LNG": -163806.07,
                    "LAT": 6610726.44,
                    "STATUS": "HISTORICAL",
                    "LOGICAL_STATUS_CODE": "8",
                    "CLASSIFICATION_CODE": "CI01",
                    "CLASSIFICATION_CODE_DESCRIPTION": "Factory/Manufacturing",
                    "LOCAL_CUSTODIAN_CODE": 1760,
                    "LOCAL_CUSTODIAN_CODE_DESCRIPTION": "TEST VALLEY",
                    "POSTAL_ADDRESS_CODE": "D",
                    "POSTAL_ADDRESS_CODE_DESCRIPTION": "A record which is linked to PAF",
                    "BLPU_STATE_CODE": "null",
                    "BLPU_STATE_CODE_DESCRIPTION": "Unknown/Not applicable",
                    "TOPOGRAPHY_LAYER_TOID": "osgb5000005278503035",
                    "PARENT_UPRN": "10094212626",
                    "LAST_UPDATE_DATE": "01/09/2021",
                    "ENTRY_DATE": "20/08/2019",
                    "LANGUAGE": "EN",
                    "MATCH": 0.4,
                    "MATCH_DESCRIPTION": "NO MATCH",
                },
            },
        ),
        param(
            {
                "X_COORDINATE": 437230.0,
                "Y_COORDINATE": 115775.0,
                "test": "x",
                "test2": 6610726.44,
            },
            "EPSG:27700",
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [437230.0, 115775.0]},
                "properties": {
                    "X_COORDINATE": 437230.0,
                    "Y_COORDINATE": 115775.0,
                    "test": "x",
                    "test2": 6610726.44,
                },
            },
        ),
    ]
    return test_variables, test_data


def test_address_to_feature_error():
    test_variables = "address, crs"
    test_data = [
        param(
            {
                "X_COORDINATE": 437230.0,
                "Y_COORDINATE": 115775.0,
                "test": "x",
                "test2": 6610726.44,
            },
            "EPSG:3857",
        )
    ]
    return test_variables, test_data
