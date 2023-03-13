import os
import json

os.environ["OSDATAHUB_PROXIES"] = json.dumps({})

def set_proxies(proxies):
    os.environ["OSDATAHUB_PROXIES"] = json.dumps(proxies)

def get_proxies():
    return json.loads(os.environ["OSDATAHUB_PROXIES"])

__version__ = "1.2.1"

from osdatahub.extent import Extent
from osdatahub.FeaturesAPI import FeaturesAPI
from osdatahub.PlacesAPI import PlacesAPI
from osdatahub.NamesAPI import NamesAPI
from osdatahub.LinkedIdentifiersAPI import LinkedIdentifiersAPI
from osdatahub.DownloadsAPI import OpenDataDownload, DataPackageDownload
from osdatahub.NGD import NGD
