from pytest import param

from osdatahub import Extent
from osdatahub.filters import is_between, intersects


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
    ]
    return test_variables, test_data
