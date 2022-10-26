from typing import Union
import datetime

from geojson import FeatureCollection

from osdatahub import Extent
from osdatahub.bbox import BBox


class NGD:
    ENDPOINT = r"https://api.os.uk/features/ngd/ofa/v1/"

    DEFAULTS = {

    }

    def __init__(self, key: str, collection: str, extent: Extent):
        self.key: str = key,
        self.collection: str = collection,
        self.extent = extent

    def query(self,
              feature_id: str = None,
              crs: Union[str, int] = None,
              start_datetime: datetime = None,
              end_datetime: datetime = None,
              filter = None,
              filter_crs: Union[str, int] = None,
              bbox_crs: Union[str, int] = None,
              limit: int = 100,
              offset: int = 0) -> FeatureCollection:
        # TODO: implement
        pass


