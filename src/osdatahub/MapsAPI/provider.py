from warnings import warn
from xyzservices import TileProvider
from datetime import datetime


AvailableLayers = [
    'Road_3857', 'Road_27700',
    'Outdoor_3857', 'Outdoor_27700',
    'Light_3857', 'Light_27700',
    'Leisure_27700',
]


class OSTileProvider(TileProvider):
    """
    Main class for using OS MapsAPI
    (https://osdatahub.os.uk/docs/wmts/)

    Args:
        key (str): A valid OS MapsAPI key.
        layer (str): A valid Layer Name in the format <Style>_<projection>, Default "Light_3857", Options `osdatahub.MapsAPI.AvailableLayers`.
    Returns:
        OSTileProvider (TileProvider)

    Examples
    --------
    AvailableLayers
    >>> from osdatahub.MapsAPI import AvailableLayers
    >>> print(AvailableLayers)
    OSTileProvider
    >>> from osdatahub.MapsAPI import OSTileProvider
    >>> provider = OSTileProvider(key, 'Light_3857')
    Contextily
    >>> ctx.add_basemap(ax=ax, provider=provider)
    Folium
    >>> m = folium.Map(tile=provider)
    """
    def __init__(self, key: str, layer: str = 'Light_3857', **kwargs):
        assert layer in AvailableLayers, f'{layer} not in AvailableLayers: {", ".join(AvailableLayers)}'
        if layer.endswith('_27700'): warn(f'{layer}, CRS=EPSG:27700 is not recognised by contextily or folium.')
        super().__init__({
            'name': f'OS Maps {layer}',
            'url': f'https://api.os.uk/maps/raster/v1/zxy/{layer}/{{z}}/{{x}}/{{y}}.png?key={key}',
            'max_zoom': 16,
            'attribution': f'Contains OS data © Crown copyright and database right {datetime.now().year}',
        }, **kwargs)
