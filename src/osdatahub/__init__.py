import os
import json
import logging

os.environ["_OSDATAHUB_PROXIES"] = json.dumps({})

def set_proxies(proxies):
    os.environ["_OSDATAHUB_PROXIES"] = json.dumps(proxies)

def get_proxies():
    return json.loads(os.environ["_OSDATAHUB_PROXIES"])

__version__ = "1.2.11"

from osdatahub.extent import Extent
from osdatahub.FeaturesAPI import FeaturesAPI
from osdatahub.PlacesAPI import PlacesAPI
from osdatahub.NamesAPI import NamesAPI
from osdatahub.LinkedIdentifiersAPI import LinkedIdentifiersAPI
from osdatahub.DownloadsAPI import OpenDataDownload, DataPackageDownload
from osdatahub.NGD import NGD
from osdatahub.requests_wrapper import get, post