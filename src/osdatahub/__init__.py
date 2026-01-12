import json
import logging
import os

os.environ["_OSDATAHUB_PROXIES"] = json.dumps({})


def set_proxies(proxies):
    os.environ["_OSDATAHUB_PROXIES"] = json.dumps(proxies)


def get_proxies():
    return json.loads(os.environ["_OSDATAHUB_PROXIES"])

__version__ = "1.3.3"

from osdatahub.DownloadsAPI import DataPackageDownload, OpenDataDownload
from osdatahub.extent import Extent
from osdatahub.FeaturesAPI import FeaturesAPI
from osdatahub.LinkedIdentifiersAPI import LinkedIdentifiersAPI
from osdatahub.NamesAPI import NamesAPI
from osdatahub.NGD import NGD, AsyncNGD
from osdatahub.PlacesAPI import PlacesAPI
from osdatahub.requests_wrapper import get, post
