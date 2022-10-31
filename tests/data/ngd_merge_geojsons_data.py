from pytest import param

geojson_1_feature = {
    "type": "FeatureCollection",
    "links": [
        {
            "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items?limit=1",
            "rel": "self",
            "type": "application/geo+json",
            "title": "All features from the 'Building Line' collection"
        },
        {
            "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items?offset=1&limit=1",
            "rel": "next",
            "type": "application/geo+json",
            "title": "Next page"
        }
    ],
    "timeStamp": "2022-10-28T14:20:26.387528Z",
    "numberReturned": 1,
    "features": [
        {
            "id": "00000016-e0a2-45ca-855a-645753d72716",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.8649573,
                        51.8129786
                    ],
                    [
                        -3.8649033,
                        51.8129757
                    ]
                ]
            },
            "properties": {
                "osid": "00000016-e0a2-45ca-855a-645753d72716",
                "toid": "osgb5000005271044468",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 3.734355,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2020-09-23",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2019-07-05",
                "description_updatedate": "2020-09-23",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "2020-09-23",
                "description_evidencedate": "2019-07-05",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        }
    ]
}

geojson_10_features = {
    "type": "FeatureCollection",
    "links": [
        {
            "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items?limit=10",
            "rel": "self",
            "type": "application/geo+json",
            "title": "All features from the 'Building Line' collection"
        },
        {
            "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items?offset=10&limit=10",
            "rel": "next",
            "type": "application/geo+json",
            "title": "Next page"
        }
    ],
    "timeStamp": "2022-10-28T14:21:21.524232Z",
    "numberReturned": 10,
    "features": [
        {
            "id": "00000016-e0a2-45ca-855a-645753d72716",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.8649573,
                        51.8129786
                    ],
                    [
                        -3.8649033,
                        51.8129757
                    ]
                ]
            },
            "properties": {
                "osid": "00000016-e0a2-45ca-855a-645753d72716",
                "toid": "osgb5000005271044468",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 3.734355,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2020-09-23",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2019-07-05",
                "description_updatedate": "2020-09-23",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "2020-09-23",
                "description_evidencedate": "2019-07-05",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "00000052-e07e-4420-b2d5-b6ff90afcac2",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.0641844,
                        50.9584926
                    ],
                    [
                        -3.0643669,
                        50.9585053
                    ]
                ]
            },
            "properties": {
                "osid": "00000052-e07e-4420-b2d5-b6ff90afcac2",
                "toid": "osgb1000000283880279",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Overhanging Building Edge",
                "versiondate": "2022-08-26",
                "physicallevel": "Level 1",
                "geometry_length": 12.899612,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2004-01-28",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2004-01-28",
                "description_updatedate": "2004-01-28",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1992-02-01",
                "description_evidencedate": "2004-01-28",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "000000b7-a66f-42b5-870b-3ea9729b73e3",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -1.2987328,
                        54.0082184
                    ],
                    [
                        -1.2987991,
                        54.0081463
                    ]
                ]
            },
            "properties": {
                "osid": "000000b7-a66f-42b5-870b-3ea9729b73e3",
                "toid": "osgb1000000080069326",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 9.130049,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2007-02-20",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2007-02-20",
                "description_updatedate": "2007-02-20",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1992-09-24",
                "description_evidencedate": "2007-02-20",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "00000102-d65c-4396-8635-6f0a049023d9",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -1.9501576,
                        52.5456803
                    ],
                    [
                        -1.9501459,
                        52.5456862
                    ],
                    [
                        -1.95005,
                        52.5457325
                    ]
                ]
            },
            "properties": {
                "osid": "00000102-d65c-4396-8635-6f0a049023d9",
                "toid": "osgb1000000124252224",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Occupier Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 9.324264,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2016-08-01",
                "capturespecification": "Urban",
                "geometry_evidencedate": "2016-04-20",
                "description_updatedate": "1983-10-13",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1983-10-13",
                "description_evidencedate": "1983-10-13",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "0000013e-5fed-447d-a627-dae6fb215138",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.3809754,
                        52.2413303
                    ],
                    [
                        -3.3809517,
                        52.2413255
                    ]
                ]
            },
            "properties": {
                "osid": "0000013e-5fed-447d-a627-dae6fb215138",
                "toid": "osgb1000000264266704",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 1.707923,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2005-06-22",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2005-06-22",
                "description_updatedate": "2005-06-22",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1992-04-13",
                "description_evidencedate": "2005-06-22",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "0000031f-f2d0-4547-8d91-715e8073a00b",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -0.4105347,
                        53.7419995
                    ],
                    [
                        -0.4105707,
                        53.7420023
                    ]
                ]
            },
            "properties": {
                "osid": "0000031f-f2d0-4547-8d91-715e8073a00b",
                "toid": "osgb1000000012849650",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 2.39416,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2009-05-29",
                "capturespecification": "Urban",
                "geometry_evidencedate": "2009-05-29",
                "description_updatedate": "2009-05-29",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1999-06-11",
                "description_evidencedate": "2009-05-29",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "0000037a-4ece-460c-add7-5cd68ec700e9",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        0.1697308,
                        51.7160161
                    ],
                    [
                        0.1698108,
                        51.7160542
                    ],
                    [
                        0.1698501,
                        51.7160727
                    ]
                ]
            },
            "properties": {
                "osid": "0000037a-4ece-460c-add7-5cd68ec700e9",
                "toid": "osgb1000000027690091",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Occupier Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 10.375383,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2021-07-21",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2021-07-21",
                "description_updatedate": "2002-12-11",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1994-06-29",
                "description_evidencedate": "2002-12-11",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "000003f7-455e-4a1f-9691-29c927a3687f",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -0.1789267,
                        51.3667955
                    ],
                    [
                        -0.1789231,
                        51.3667956
                    ],
                    [
                        -0.1788968,
                        51.3667965
                    ],
                    [
                        -0.1787859,
                        51.366799
                    ]
                ]
            },
            "properties": {
                "osid": "000003f7-455e-4a1f-9691-29c927a3687f",
                "toid": "osgb1000001798457344",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Occupier Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 9.811248,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2017-09-04",
                "capturespecification": "Urban",
                "geometry_evidencedate": "2016-09-15",
                "description_updatedate": "1970-01-01",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1970-01-01",
                "description_evidencedate": "1970-01-01",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "0000046d-6491-4f76-8d61-a7080b9b83e4",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -2.198468,
                        52.1985489
                    ],
                    [
                        -2.1984579,
                        52.1985368
                    ]
                ]
            },
            "properties": {
                "osid": "0000046d-6491-4f76-8d61-a7080b9b83e4",
                "toid": "osgb1000002071113695",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Overhanging Building Edge",
                "versiondate": "2022-08-26",
                "physicallevel": "Level 1",
                "geometry_length": 1.507216,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "1989-10-24",
                "capturespecification": "Urban",
                "geometry_evidencedate": "1989-10-24",
                "description_updatedate": "1989-10-24",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1989-10-24",
                "description_evidencedate": "1989-10-24",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "00000471-3f43-4cfb-a506-9e9c862b113c",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -1.4225073,
                        53.3766972
                    ],
                    [
                        -1.4224614,
                        53.3767604
                    ]
                ]
            },
            "properties": {
                "osid": "00000471-3f43-4cfb-a506-9e9c862b113c",
                "toid": "osgb1000000107792612",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Occupier Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 7.661756,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "1993-03-01",
                "capturespecification": "Urban",
                "geometry_evidencedate": "1993-03-01",
                "description_updatedate": "1993-03-01",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1993-03-01",
                "description_evidencedate": "1993-03-01",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        }
    ]
}

geojson_3_features = {
    "type": "FeatureCollection",
    "links": [
        {
            "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items?limit=3",
            "rel": "self",
            "type": "application/geo+json",
            "title": "All features from the 'Building Line' collection"
        },
        {
            "href": "https://api.os.uk/features/ngd/ofa/v1/collections/bld-fts-buildingline/items?offset=3&limit=3",
            "rel": "next",
            "type": "application/geo+json",
            "title": "Next page"
        }
    ],
    "timeStamp": "2022-10-28T14:21:50.334565Z",
    "numberReturned": 3,
    "features": [
        {
            "id": "00000016-e0a2-45ca-855a-645753d72716",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.8649573,
                        51.8129786
                    ],
                    [
                        -3.8649033,
                        51.8129757
                    ]
                ]
            },
            "properties": {
                "osid": "00000016-e0a2-45ca-855a-645753d72716",
                "toid": "osgb5000005271044468",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 3.734355,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2020-09-23",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2019-07-05",
                "description_updatedate": "2020-09-23",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "2020-09-23",
                "description_evidencedate": "2019-07-05",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "00000052-e07e-4420-b2d5-b6ff90afcac2",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -3.0641844,
                        50.9584926
                    ],
                    [
                        -3.0643669,
                        50.9585053
                    ]
                ]
            },
            "properties": {
                "osid": "00000052-e07e-4420-b2d5-b6ff90afcac2",
                "toid": "osgb1000000283880279",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Overhanging Building Edge",
                "versiondate": "2022-08-26",
                "physicallevel": "Level 1",
                "geometry_length": 12.899612,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2004-01-28",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2004-01-28",
                "description_updatedate": "2004-01-28",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1992-02-01",
                "description_evidencedate": "2004-01-28",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        },
        {
            "id": "000000b7-a66f-42b5-870b-3ea9729b73e3",
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [
                        -1.2987328,
                        54.0082184
                    ],
                    [
                        -1.2987991,
                        54.0081463
                    ]
                ]
            },
            "properties": {
                "osid": "000000b7-a66f-42b5-870b-3ea9729b73e3",
                "toid": "osgb1000000080069326",
                "theme": "Buildings",
                "changetype": "New",
                "isobscured": "false",
                "description": "Building Internal Division",
                "versiondate": "2022-08-26",
                "physicallevel": "Surface Level",
                "geometry_length": 9.130049,
                "geometry_source": "Ordnance Survey",
                "description_source": "Ordnance Survey",
                "geometry_updatedate": "2007-02-20",
                "capturespecification": "Rural",
                "geometry_evidencedate": "2007-02-20",
                "description_updatedate": "2007-02-20",
                "versionavailabletodate": "null",
                "firstdigitalcapturedate": "1992-09-24",
                "description_evidencedate": "2007-02-20",
                "versionavailablefromdate": "2022-08-27T00:00:00Z"
            }
        }
    ]
}


def test_merge_geojsons_pass():
    test_variables = "gj1, gj2, expected_result"
    test_data = [
        param(geojson_1_feature, geojson_3_features, 4),
        param(geojson_1_feature, geojson_10_features, 11),
        param(geojson_3_features, geojson_10_features, 13),
        param(geojson_3_features, {}, 3),
        param({}, geojson_10_features, 10)
    ]
    return test_variables, test_data


def test_merge_geojsons_fail():
    test_variables = "gj1, gj2, expected_result"
    test_data = [
        param({}, {}, ValueError),
        param({"hello": "world"}, {"hello": "world"}, ValueError),
        param({"hello": "world"}, geojson_10_features, ValueError)
    ]
    return test_variables, test_data
