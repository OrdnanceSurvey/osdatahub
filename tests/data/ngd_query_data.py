from datetime import datetime

from osdatahub import Extent
from pytest import param
from shapely.geometry import Polygon


def test_ngd_query():
    test_variables = "extent, crs, start_datetime, end_datetime, cql_filter, filter_crs, max_results, offset, " \
                     "expected_url, expected_params"
    test_data = [
        param(
            None,
            None,
            None,
            None,
            None,
            None,
            100,
            0,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 0
            }
        ),
        param(
            None,
            None,
            None,
            None,
            None,
            None,
            50,
            0,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 50,
                "offset": 0
            }
        ),
        param(
            None,
            None,
            None,
            None,
            None,
            None,
            100,
            20,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 20
            }
        ),
        param(Extent.from_bbox((-2.503510, 53.578646, -2.432785, 53.600655), crs="EPSG:4326"),
              None,
              None,
              None,
              None,
              None,
              100,
              0,
              r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
              {
                  "limit": 100,
                  "offset": 0,
                  "filter": "INTERSECTS(geometry, POLYGON ((-2.432785 53.578646, -2.432785 53.600655, "
                            "-2.50351 53.600655, -2.50351 53.578646, -2.432785 53.578646)))",
                  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/4326"
              }
              ),
        param(Extent.from_bbox((-278689.4051, 7090757.3659, -270816.3912, 7094884.9654), crs="EPSG:3857"),
              None,
              None,
              None,
              None,
              None,
              100,
              0,
              r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
              {
                  "limit": 100,
                  "offset": 0,
                  "filter": "INTERSECTS(geometry, POLYGON ((-270816.3912 7090757.3659, -270816.3912 7094884.9654, "
                            "-278689.4051 7094884.9654, -278689.4051 7090757.3659, -270816.3912 7090757.3659)))",
                  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
              }
              ),
        param(Extent(Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]), crs="EPSG:3857"),
              None,
              None,
              None,
              None,
              None,
              100,
              0,
              r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
              {
                  "limit": 100,
                  "offset": 0,
                  "filter": "INTERSECTS(geometry, POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0)))",
                  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
              }
              ),
        param(
            None,
            3857,
            None,
            None,
            None,
            None,
            100,
            20,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 20,
                "crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
            }
        ),
        param(
            None,
            3857,
            datetime(2014, 1, 1, 0, 0, 1),
            None,
            None,
            None,
            100,
            20,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 20,
                "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
                "datetime": "2014-01-01T00:00:01Z/.."
            }
        ),
        param(
            None,
            3857,
            None,
            datetime(2015, 1, 1, 0, 0, 1),
            None,
            None,
            100,
            20,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 20,
                "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
                "datetime": "../2015-01-01T00:00:01Z"
            }
        ),
        param(
            None,
            3857,
            datetime(2014, 1, 1, 0, 0, 1),
            datetime(2015, 1, 1, 0, 0, 1),
            None,
            None,
            100,
            20,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 20,
                "crs": "http://www.opengis.net/def/crs/EPSG/0/3857",
                "datetime": "2014-01-01T00:00:01Z/2015-01-01T00:00:01Z"
            }
        ),
        param(
            None,
            None,
            None,
            None,
            "HELLO WORLD",
            27700,
            100,
            0,
            r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
            {
                "limit": 100,
                "offset": 0,
                "filter": "HELLO WORLD",
                "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/27700"
            }
        ),
        param(Extent(Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]), crs="EPSG:3857"),
              None,
              None,
              None,
              "HELLO WORLD",
              None,
              100,
              0,
              r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
              {
                  "limit": 100,
                  "offset": 0,
                  "filter": "HELLO WORLD AND INTERSECTS(geometry, POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0)))",
                  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
              }
              ),
        param(Extent(Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]), crs="EPSG:3857"),
              None,
              None,
              None,
              "HELLO WORLD",
              "epsg:3857",
              100,
              0,
              r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
              {
                  "limit": 100,
                  "offset": 0,
                  "filter": "HELLO WORLD AND INTERSECTS(geometry, POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0)))",
                  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
              }
              ),
        param(Extent(Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]), crs="EPSG:3857"),
              7405,
              datetime(2013, 1, 3, 12, 13, 14),
              datetime(2016, 3, 2, 1, 2, 3),
              "HELLO WORLD",
              "epsg:3857",
              100,
              0,
              r"https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/",
              {
                  "limit": 100,
                  "offset": 0,
                  "crs": "http://www.opengis.net/def/crs/EPSG/0/7405",
                  "datetime": "2013-01-03T12:13:14Z/2016-03-02T01:02:03Z",
                  "filter": "HELLO WORLD AND INTERSECTS(geometry, POLYGON ((0 0, 1 0, 1 1, 0 1, 0 0)))",
                  "filter-crs": "http://www.opengis.net/def/crs/EPSG/0/3857"
              }
              ),
    ]

    return test_variables, test_data


def test_ngd_query_fail():
    test_variables = "extent, crs, start_datetime, end_datetime, cql_filter, filter_crs, max_results, offset, " \
                     "expected_error"
    test_data = [
        param(
            Extent(Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]), crs="EPSG:3857"),
            None,
            None,
            None,
            "HELLO WORLD",
            "EPSG:4326",
            100,
            0,
            AssertionError
        ),
        param(
            None,
            None,
            datetime(2014, 1, 1, 0, 0, 1),
            datetime(2013, 1, 1, 0, 0, 1),
            None,
            None,
            100,
            0,
            ValueError
        ),
        param(
            None,
            None,
            None,
            None,
            None,
            None,
            0,
            0,
            AssertionError
        ),
        param(
            None,
            None,
            None,
            None,
            None,
            None,
            1,
            -1,
            AssertionError
        ),

    ]

    return test_variables, test_data


def test_ngd_instantiation():
    test_variables = "api_key, collection, expected_url, expected_headers"
    test_data = [
        param(
            "test_key",
            "test_collection",
            "https://api.os.uk/features/ngd/ofa/v1/collections/test_collection/items/",
            {"key": "test_key", 'Accept': 'application/geo+json'}
        ),
        param(
            "test_key2",
            "test_collection2",
            "https://api.os.uk/features/ngd/ofa/v1/collections/test_collection2/items/",
            {"key": "test_key2", 'Accept': 'application/geo+json'}
        )
    ]
    return test_variables, test_data


def test_ngd_query_feature():
    test_variables = "feature_id, crs, expected_url, expected_params"
    test_data = [
        param("feature_id",
              None,
              "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/feature_id",
              {}
              ),
        param("feature_id2",
              None,
              "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/feature_id2",
              {}
              ),
        param("feature_id2",
              3857,
              "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/feature_id2",
              {"crs": "http://www.opengis.net/def/crs/EPSG/0/3857"}
              ),
        param("feature_id2",
              "epsg:7405",
              "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items/feature_id2",
              {"crs": "http://www.opengis.net/def/crs/EPSG/0/7405"}
              ),
    ]

    return test_variables, test_data



def test_ngd_query_live():
    test_variables = "collection, extent, crs, start_datetime, end_datetime, cql_filter, filter_crs, max_results, offset"
    test_data = [
        param(
            "bld-fts-buildingpart",
            None,
            None,
            None,
            None,
            None,
            None,
            5,
            0
        ),
        param(
            "lus-fts-site",
            None,
            None,
            None,
            None,
            None,
            None,
            50,
            0
        ),
        param(
            "str-fts-structureline",
            None,
            None,
            None,
            None,
            None,
            None,
            5,
            20
        ),
        param("trn-ntwk-road",
            Extent.from_bbox((-2.503510, 53.578646, -2.432785, 53.600655), crs="CRS84"),
              None,
              None,
              None,
              None,
              None,
              5,
              0
              ),
        param("trn-rami-highwaydedication",
            Extent.from_bbox((-278689.4051, 7090757.3659, -270816.3912, 7094884.9654), crs="EPSG:3857"),
              None,
              None,
              None,
              None,
              None,
              5,
              0
              ),
        param("wtr-ntwk-waterlink",
            Extent.from_bbox((280371.5367, 597854.9713, 320300.6732, 625998.9645), crs="EPSG:27700"),
              None,
              None,
              None,
              None,
              None,
              5,
              0
              ),
        param("trn-fts-rail",
            None,
            3857,
            None,
            None,
            None,
            None,
            7,
            20
        ),
        param("trn-ntwk-road",
            None,
            3857,
            None,
            None,
            None,
            None,
            134,
            20,
            id=">100 features"
        )
    ]

    return test_variables, test_data
