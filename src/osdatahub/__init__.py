import sys

this = sys.modules[__name__]
this.PROXIES = {}

def set_proxies(proxies):
    this.PROXIES = proxies

def get_proxies():
    return this.PROXIES

__version__ = "1.2.1"

from osdatahub.extent import Extent
from osdatahub.FeaturesAPI import FeaturesAPI
from osdatahub.PlacesAPI import PlacesAPI
from osdatahub.NamesAPI import NamesAPI
from osdatahub.LinkedIdentifiersAPI import LinkedIdentifiersAPI
from osdatahub.DownloadsAPI import OpenDataDownload, DataPackageDownload
from osdatahub.NGD import NGD
