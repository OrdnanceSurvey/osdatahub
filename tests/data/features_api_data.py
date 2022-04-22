from osdatahub import Extent
from osdatahub.filters import intersects, is_between
from pytest import param


def test__params():
    test_variables = "extent, product, filters, expected_result"
    test_data = [
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:27700"),
            "topographic_area",
            [],
            {
                "service": "wfs",
                "version": "2.0.0",
                "request": "GetFeature",
                "outputFormat": "geojson",
                "count": 100,
                "key": "API-KEY",
                "srsName": "EPSG:27700",
                "typeName": "Topography_TopographicArea",
                "filter": '<ogc:Filter><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects></ogc:Filter>',
            },
            id="bbox no filters",
        ),
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:27700"),
            "topographic_area",
            [
                is_between("sample name", 0, 1),
                intersects(Extent.from_bbox((0, 0, 1, 1), "EPSG:27700")),
            ],
            {
                "service": "wfs",
                "version": "2.0.0",
                "request": "GetFeature",
                "outputFormat": "geojson",
                "count": 100,
                "key": "API-KEY",
                "srsName": "EPSG:27700",
                "typeName": "Topography_TopographicArea",
                "filter": '<ogc:Filter><ogc:And><ogc:And><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects><ogc:PropertyIsBetween><ogc:PropertyName>sample name</ogc:PropertyName><LowerBoundary><ogc:Literal>0</ogc:Literal></LowerBoundary><UpperBoundary><ogc:Literal>1</ogc:Literal></UpperBoundary></ogc:PropertyIsBetween></ogc:And><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects></ogc:And></ogc:Filter>',
            },
            id="bbox with filters is_between intersects",
        ),
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:27700"),
            "Topography_TopographicArea",
            [
                is_between("sample name", 0, 1),
                intersects(Extent.from_bbox((0, 0, 1, 1), "EPSG:27700")),
            ],
            {
                "service": "wfs",
                "version": "2.0.0",
                "request": "GetFeature",
                "outputFormat": "geojson",
                "count": 100,
                "key": "API-KEY",
                "srsName": "EPSG:27700",
                "typeName": "Topography_TopographicArea",
                "filter": '<ogc:Filter><ogc:And><ogc:And><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects><ogc:PropertyIsBetween><ogc:PropertyName>sample name</ogc:PropertyName><LowerBoundary><ogc:Literal>0</ogc:Literal></LowerBoundary><UpperBoundary><ogc:Literal>1</ogc:Literal></UpperBoundary></ogc:PropertyIsBetween></ogc:And><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects></ogc:And></ogc:Filter>',
            },
            id="API style product name",
        ),
    ]
    return test_variables, test_data


def test_request_params():
    test_variables = "extent, product, filters, limit, expected_url, expected_params"
    test_data = [
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:27700"),
            "topographic_area",
            [],
            100,
            "https://api.os.uk/features/v1/wfs",
            {
                "service": "wfs",
                "version": "2.0.0",
                "request": "GetFeature",
                "outputFormat": "geojson",
                "key": "API-KEY",
                "srsName": "EPSG:27700",
                "typeName": "Topography_TopographicArea",
                "filter": '<ogc:Filter><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects></ogc:Filter>',
                "count": 100,
                "startIndex": 0
            },
            id="bbox no filters - limit=100",
        ),
        param(
            Extent.from_bbox((0, 0, 1, 1), "EPSG:27700"),
            "topographic_area",
            [],
            50,
            "https://api.os.uk/features/v1/wfs",
            {
                "service": "wfs",
                "version": "2.0.0",
                "request": "GetFeature",
                "outputFormat": "geojson",
                "key": "API-KEY",
                "srsName": "EPSG:27700",
                "typeName": "Topography_TopographicArea",
                "filter": '<ogc:Filter><ogc:Intersects><ogc:PropertyName>SHAPE</ogc:PropertyName><gml:Polygon xmlns:gml=\'http://www.opengis.net/gml\' srsName=\'EPSG:27700\'><gml:outerBoundaryIs><gml:LinearRing><gml:coordinates decimal="." cs="," ts=" ">1.0,0.0 1.0,1.0 0.0,1.0 0.0,0.0 1.0,0.0</gml:coordinates></gml:LinearRing></gml:outerBoundaryIs></gml:Polygon></ogc:Intersects></ogc:Filter>',
                "count": 50,
                "startIndex": 0
            },
            id="bbox no filters - limit=50",
        ),
    ]
    return test_variables, test_data


def test_query():
    test_variables = "product, extent, limit, expected_count"
    test_data = [
        param(
            "topographic_area",
            Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700"),
            100,
            100,
            id="bbox, topographic_area, limit=100",
        ),
        param(
            "topographic_area",
            Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700"),
            12,
            12,
            id="bbox, topographic_area, limit=12",
        ),
        param(
            "Topography_TopographicArea",
            Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700"),
            12,
            12,
            id="bbox, Topography_TopographicArea, limit=12",
        ),
        param(
            "topographic_area",
            Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700"),
            200,
            200,
            id="bbox, topographic_area, limit=200",
        ),
    ]
    return test_variables, test_data
