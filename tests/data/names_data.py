from osdatahub.extent import Extent
from pytest import param
from typeguard import TypeCheckError


def test_format_fq():
    test_variables = "bbox, local_type, expected_result"
    test_data = [
        param(None,
              "oil_refining",
              ["LOCAL_TYPE:Oil_Refining"]),
        param(None,
              "special_needs_education",
              ["LOCAL_TYPE:Special_Needs_Education"]),
        param(None,
              ["town", "road_user_services"],
              ["LOCAL_TYPE:Town LOCAL_TYPE:Road_User_Services"]),
        param(None,
              ["hill_or_mountain", "heliport", "postcode",
                  "bay", "electricity_distribution"],
              ["LOCAL_TYPE:Hill_Or_Mountain LOCAL_TYPE:Heliport LOCAL_TYPE:Postcode LOCAL_TYPE:Bay "
               "LOCAL_TYPE:Electricity_Distribution"]),
        param(Extent.from_bbox((1000, 1000, 2000, 2000), crs="EPSG:27700"),
              None,
              ["BBOX:1000.0,1000.0,2000.0,2000.0"]),
        param(Extent.from_bbox((10000, 20000, 30000, 40000), crs="EPSG:27700"),
              None,
              ["BBOX:10000.0,20000.0,30000.0,40000.0"]),
        param(Extent.from_bbox((10000, 20000, 30000, 40000), crs="EPSG:27700"),
              "estuary",
              ["LOCAL_TYPE:Estuary", "BBOX:10000.0,20000.0,30000.0,40000.0"]),
        param(Extent.from_bbox((1000, 1000, 2000, 2000), crs="EPSG:27700"),
              ["other_settlement", "passenger_ferry_terminal", "spot_height"],
              ["LOCAL_TYPE:Other_Settlement LOCAL_TYPE:Passenger_Ferry_Terminal LOCAL_TYPE:Spot_Height",
               "BBOX:1000.0,1000.0,2000.0,2000.0"]),

    ]
    return test_variables, test_data


def test_format_fq_errors():
    test_variables = "bbox, local_type, expected_result"
    test_data = [
        param(None,
              1234,
              (TypeError,TypeCheckError)),
        param(1234,
              None,
              (TypeError,TypeCheckError)),
        param(None,
              "fake_local_type",
              ValueError),
        param(None,
              ["town", "estuary", "fake_local_type"],
              ValueError),
        param(Extent.from_bbox((1000, 2000, 3000, 4000), crs="EPSG:4326"),
              None,
              ValueError)
    ]
    return test_variables, test_data


def test_find_pass():
    test_variables = "text, limit, bounds, bbox_filter, local_type, expected_url, expected_params"
    test_data = [
        param("Buckingham Palace",
              100,
              None,
              None,
              None,
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "maxresults": 100}
              ),
        param("OS HQ",
              100,
              None,
              None,
              None,
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "OS HQ", "offset": 0, "maxresults": 100}
              ),
        param("Buckingham Palace",
              50,
              None,
              None,
              None,
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "maxresults": 50}
              ),
        param("Buckingham Palace",
              50,
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:27700"),
              None,
              None,
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0,
                  "bounds": "100.0,200.0,300.0,400.0", "maxresults": 50}
              ),
        param("Buckingham Palace",
              50,
              None,
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:27700"),
              None,
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "fq": [
                  "BBOX:100.0,200.0,300.0,400.0"], "maxresults": 50}
              ),
        param("Buckingham Palace",
              50,
              None,
              None,
              "suburban_area",
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "fq": [
                  "LOCAL_TYPE:Suburban_Area"], "maxresults": 50}
              ),
        param("Buckingham Palace",
              50,
              None,
              None,
              ("suburban_area", "tramway"),
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "fq": ["LOCAL_TYPE:Suburban_Area LOCAL_TYPE:Tramway"],
               "maxresults": 50}
              ),
        param("Buckingham Palace",
              50,
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:27700"),
              None,
              "suburban_area",
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "bounds": "100.0,200.0,300.0,400.0",
               "fq": ["LOCAL_TYPE:Suburban_Area"], "maxresults": 50}
              ),
        param("Buckingham Palace",
              50,
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:27700"),
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:27700"),
              "suburban_area",
              'https://api.os.uk/search/names/v1/find?key=test',
              {"query": "Buckingham Palace", "offset": 0, "bounds": "100.0,200.0,300.0,400.0",
               "fq": ["LOCAL_TYPE:Suburban_Area", "BBOX:100.0,200.0,300.0,400.0"], "maxresults": 50}
              )
    ]
    return test_variables, test_data


def test_find_live():
    test_variables = "text, limit, expected_length, minimum_length"
    test_data = [
        param("AB22 9", 100, 100, None),
        param("AB22 9", 47, 47, None),
        param("AB22 9", 1000, None, 100),
    ]
    return test_variables, test_data


def test_find_fail():
    test_variables = "text, limit, bounds, bbox_filter, local_type, expected_result"
    test_data = [
        param("Buckingham Palace",
              -1,
              None,
              None,
              None,
              ValueError
              ),
        param("Buckingham Palace",
              50,
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:4326"),
              None,
              None,
              (TypeError, TypeCheckError)
              ),
        param("Buckingham Palace",
              50,
              None,
              Extent.from_bbox((100, 200, 300, 400), crs="EPSG:4326"),
              None,
              (TypeError,TypeCheckError)
              ),
        param("Buckingham Palace",
              50,
              None,
              None,
              "testtest",
              ValueError),
    ]
    return test_variables, test_data


def test_nearest_pass():
    test_variables = "point, radius, local_type, expected_url, expected_params"
    test_data = [
        param(
            (100, 200),
            100,
            None,
            'https://api.os.uk/search/names/v1/nearest?key=test',
            {"point": "100,200", "radius": 100}
        ),
        param(
            (1000, 2000),
            100,
            None,
            'https://api.os.uk/search/names/v1/nearest?key=test',
            {"point": "1000,2000", "radius": 100}
        ),
        param(
            (100, 200),
            500,
            None,
            'https://api.os.uk/search/names/v1/nearest?key=test',
            {"point": "100,200", "radius": 500}
        ),
        param(
            (100, 200),
            100,
            None,
            'https://api.os.uk/search/names/v1/nearest?key=test',
            {"point": "100,200", "radius": 100}
        ),
        param(
            (100, 200),
            100,
            "oil_refining",
            'https://api.os.uk/search/names/v1/nearest?key=test',
            {"point": "100,200", "radius": 100,
                "fq": ["LOCAL_TYPE:Oil_Refining"]}
        ),
        param(
            (100, 200),
            100,
            ("oil_refining", "oil_terminal"),
            'https://api.os.uk/search/names/v1/nearest?key=test',
            {"point": "100,200", "radius": 100, "fq": [
                "LOCAL_TYPE:Oil_Refining LOCAL_TYPE:Oil_Terminal"]}
        )
    ]
    return test_variables, test_data


def test_nearest_fail():
    test_variables = "point, radius, local_type, expected_result"
    test_data = [
        param(
            ("dog", "cat"),
            100,
            None,
            (TypeError, TypeCheckError)
        ),
        param(
            (100, 200),
            1001,
            None,
            ValueError
        ),
        param(
            (100, 200),
            -5,
            None,
            ValueError
        ),
        param(
            (100, 200),
            100,
            "testtest",
            ValueError
        ),
        param(
            (100, 200),
            100,
            ["suburban_area", "testest"],
            ValueError
        )
    ]
    return test_variables, test_data
