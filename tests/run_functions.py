"""
Script that queries all places and features endpoints that are implemented 
in osdatahub.

This is just for convenience and is intentionally left unrecognisable to 
pytest. Otherwise, running tests could cost developers real money!
"""

from os import environ

from osdatahub import Extent, FeaturesAPI, PlacesAPI, LinkedIdentifiersAPI

# Get API key
key = environ.get("OS_API_KEY")

# Set extent
extent = Extent.from_bbox((600000, 310200, 600900, 310900), "EPSG:27700")

print(f"{'Running':=^40}")

"""
======= FeaturesAPI =======
"""

features = FeaturesAPI(key, "zoomstack_local_buildings", extent)
results = features.query(limit=1)

assert (
        len(results["features"]) == 1
), f"FeaturesAPI.query() FAILED: {len(results['features']) = }"
print(f"FeaturesAPI.query(){'PASSED':.>20}")

"""
======= PlacesAPI =======
"""

# query
places = PlacesAPI(key)
results = places.query(extent, limit=1)

assert (
        len(results["features"]) == 1
), f"PlacesAPI.query() FAILED: {len(results['features']) = }"
print(f"PlacesAPI.query(){'PASSED':.>20}")

# find
places = PlacesAPI(key)
results = places.find(
    "test", classification_code=("CI04"), logical_status_code=1, limit=1
)

assert (
        len(results["features"]) == 1
), f"PlacesAPI.find() failed: {len(results['features']) = }"
print(f"PlacesAPI.find(){'PASSED':.>20}")

# postcode
places = PlacesAPI(key)
results = places.postcode(
    "SO21", classification_code=("RD02", "RD04"), logical_status_code=1, limit=1
)

assert (
        len(results["features"]) == 1
), f"PlacesAPI.postcode() FAILED: {len(results['features']) = }"
print(f"PlacesAPI.postcode(){'PASSED':.>20}")

# uprn
places = PlacesAPI(key)
results = places.uprn(100062015780)

assert (
        len(results["features"]) == 1
), f"PlacesAPI.uprn() FAILED: {len(results['features']) = }"
print(f"PlacesAPI.uprn(){'PASSED':.>20}")

# nearest
places = PlacesAPI(key)
results = places.nearest((600000, 310200), "EPSG:27700", radius=500)

assert (
        len(results["features"]) == 1
), f"PlacesAPI.nearest() FAILED: {len(results['features']) = }"
print(f"PlacesAPI.nearest(){'PASSED':.>20}")

"""
======= LinkedIdentifiersAPI =======
"""

# query id
linked_id = LinkedIdentifiersAPI(key)
results = linked_id.query(80833669)

assert (
        len(results["linkedIdentifiers"]) == 1
), f"LinkedIdentifiersAPI.query() FAILED: {len(results['linkedIdentifiers']) = }"
print(f"LinkedIdentifiersAPI.query(){'PASSED':.>20}")

# query id and feature_type
linked_id = LinkedIdentifiersAPI(key)
results = linked_id.query(80833669, feature_type="Street")

assert (
        len(results["linkedIdentifier"]) == 3
), f"LinkedIdentifiersAPI.query(feature_type) FAILED: {len(results['linkedIdentifier']) = }"
print(f"LinkedIdentifiersAPI.query(feature_type){'PASSED':.>20}")

# query id and identifier_type
linked_id = LinkedIdentifiersAPI(key)
results = linked_id.query(80833669, identifier_type="USRN")

assert (
        len(results["linkedIdentifier"]) == 3
), f"LinkedIdentifiersAPI.query(identifier_type) FAILED: {len(results['linkedIdentifier']) = }"
print(f"LinkedIdentifiersAPI.query(identifier_type){'PASSED':.>20}")

print(f"{'Complete':=^40}")
