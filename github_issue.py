from osdatahub import Extent, FeaturesAPI
from osdatahub.filters import is_equal
import os

lat = 123435
long = 77654

distance_metres = 1
extent = Extent.from_radius((lat, long), distance_metres, crs="EPSG:27700")

features_api = FeaturesAPI(os.environ.get("OS_API_KEY"), "Topography_TopographicArea", extent)

buildings_only = is_equal("Theme", "Buildings")
features_api.add_filters(buildings_only)

results = features_api.query(limit=1000)