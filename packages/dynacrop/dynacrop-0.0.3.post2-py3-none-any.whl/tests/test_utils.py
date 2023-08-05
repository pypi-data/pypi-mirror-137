import math
import os
import shutil
from datetime import date, timedelta
from functools import partial
from random import choice, randrange, uniform

import pyproj  # type: ignore
import requests
from dynacrop.processing_request_base import ProcessingRequest
from dynacrop import (FieldZonation, Config, Layer,
                      FieldZonationByMedian, Observation, TimeSeries)
from shapely.geometry import Point  # type: ignore
from shapely.ops import transform  # type: ignore


def authenticate():
    config = Config()
    config.api_key = 'api_key'


def supply_polygon() -> str:
    """Constructs and supplies a small random polygon within central European
    coordinates.

    Returns:
        str: Polygon in Well-Known Text.
    """
    size = 1000
    proj = partial(
        pyproj.transform,
        pyproj.Proj('epsg:4326'),
        pyproj.Proj('epsg:3857')
    )
    proj_back = partial(
        pyproj.transform,
        pyproj.Proj('epsg:3857'),
        pyproj.Proj('epsg:4326')
    )
    centre_point = Point(uniform(15, 16), uniform(48, 50))
    centre_point_3857 = transform(proj, centre_point)
    sample_polygon = centre_point_3857.buffer(math.sqrt(size) / 2).envelope
    sample_polygon_4326 = transform(proj_back, sample_polygon)
    return sample_polygon_4326.wkt


def supply_layer() -> Layer:
    """Supplies a random layer from DynaCrop Layers.

    Returns:
        Layer: Random DynaCrop Layer
    """
    return choice([layer for layer in list(Layer) if layer != Layer.SMI])


def supply_dates() -> tuple:
    """Supplies random dates from 1 to 3 months apart within Sentinel
    satellite operation years.

    Returns:
        tuple: consists of date from and date to
    """
    # Get random year within Sentinel operation
    random_year = randrange(2018, 2022)
    # Prepare range of the whole year for random date
    start_date = date(random_year, 1, 1)
    end_date = date(random_year, 12, 31)
    # Select random number (seed) of days from the prepared range
    days_between_dates = (end_date - start_date).days
    random_number_of_days = randrange(days_between_dates)

    # Create date to (add this random number to start date)
    date_to = start_date + timedelta(days=random_number_of_days)

    # Create date from (subtract 1 up to 3 months from date to)
    date_from = date.fromordinal(date_to.toordinal() - randrange(30, 120))

    return str(date_from), str(date_to)


def fetch_results(proc_req: ProcessingRequest):
    """Fires and checks all possible
    result outputs including saving them to temporary folder.
    Decides appropriately based on processing
    request type.

    Args:
        proc_req (ProcessingRequest): One of the DynaCrop processing requests.
    """
    # Creates temporary folder for checking storing
    # results
    temp_result_dir = './tmp_healthcheck'
    if not os.path.isdir(temp_result_dir):
        os.mkdir(temp_result_dir)

    if isinstance(proc_req, TimeSeries):
        proc_req.get_json()
        proc_req.save_json('tmp_healthcheck/healthcheck_result.json')
    else:
        proc_req.as_array()
        proc_req.as_geodataframe()
        proc_req.save_tiff('tmp_healthcheck/healthcheck_result.tiff')
        proc_req.save_colored_tiff(
            'tmp_healthcheck/healthcheck_result_colored.tiff')
        proc_req.save_png('tmp_healthcheck/healthcheck_result.png')
        proc_req.save_shapefile('tmp_healthcheck/healthcheck_result.shp')
        proc_req.save_geojson('tmp_healthcheck/healthcheck_result.geojson')
        requests.head(proc_req.get_demo_tiles_url()).raise_for_status()

        if isinstance(proc_req, FieldZonation) \
           or isinstance(proc_req, FieldZonationByMedian):
            proc_req.save_simplified_shapefile(
                'tmp_healthcheck/healthcheck_result.shp')
            proc_req.save_simplified_geojson(
                'tmp_healthcheck/healthcheck_result.geojson')

        proc_req.get_frequencies()

        if isinstance(proc_req, Observation):
            proc_req._get_stats()

    # Removes temporary folder
    if os.path.isdir(temp_result_dir):
        shutil.rmtree(temp_result_dir)
