import os
from enum import Enum

# TODO constants to Config
BASEURL = 'https://api-dynacrop.worldfromspace.cz/api/v2'
MAX_WAIT_TIME = 30
CONFIG_PATH: str = os.path.join(
        os.path.expanduser('~'),
        '.dynacrop'
    )
CONFIG_FILENAME = os.path.join(CONFIG_PATH, 'config.json')

# Create config folder
if not os.path.isdir(CONFIG_PATH):
    os.mkdir(CONFIG_PATH)


class CRS(Enum):
    EPSG4326 = 'EPSG:4326'


class Layer(Enum):
    NDVI = 'NDVI'
    EVI = 'EVI'
    FAPAR = 'FAPAR'
    LAI = 'LAI'
    NDMI = 'NDMI'
    CCC = 'CCC'
    CWC = 'CWC'
    NDWI = 'NDWI'
    MSAVI2 = 'MSAVI2'
    NDRE = 'NDRE'
    NDREX = 'NDREX'
    SMI = 'SMI'
    IRECI = 'IRECI'
    NDDI = 'NDDI'
    NMDI = 'NMDI'
    MNDWI = 'MNDWI'
    WIW = 'WIW'


class RenderingType(Enum):
    OBSERVATION = 'observation'
    TIME_SERIES = 'time_series'
    FIELD_ZONATION = 'field_zonation'
    FIELD_ZONATION_BY_MEDIAN = 'field_zonation_by_median'


class Result(Enum):
    RAW = "raw"
    COLOR = "color"
    PNG = "png"
    TILES_COLOR = "tiles_color"
    TILES_DEMO = "tiles_demo"
    SHP = "shp"
    GEOJSON = "geojson"
    SHP_SIMPLIFIED = "shp_simplified"
    GEOJSON_SIMPLIFIED = "geojson_simplified"
    JSON = "json"
    STATISTICS = "statistics"
    FREQUENCIES = "frequencies"
