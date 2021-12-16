from pytest import param

from osdatahub.extent import Extent


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
              ["hill_or_mountain", "heliport", "postcode", "bay", "electricity_distribution"],
              ["LOCAL_TYPE:Hill_Or_Mountain LOCAL_TYPE:Heliport LOCAL_TYPE:Postcode LOCAL_TYPE:Bay "
               "LOCAL_TYPE:Electricity_Distribution"]),
        param(Extent.from_bbox((1000,1000,2000,2000), crs="EPSG:27700"),
              None,
              ["BBOX:1000.0,1000.0,2000.0,2000.0"]),
        param(Extent.from_bbox((10000,20000,30000,40000), crs="EPSG:27700"),
              None,
              ["BBOX:10000.0,20000.0,30000.0,40000.0"]),
        param(Extent.from_bbox((10000,20000,30000,40000), crs="EPSG:27700"),
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
              TypeError),
        param(1234,
              None,
              TypeError),
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