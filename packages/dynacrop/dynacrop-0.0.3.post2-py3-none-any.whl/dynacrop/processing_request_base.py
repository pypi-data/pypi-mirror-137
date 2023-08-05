from __future__ import annotations

import json
import webbrowser
from datetime import datetime
from json.decoder import JSONDecodeError

import fiona  # type: ignore
import geopandas as gpd  # type: ignore
import numpy as np  # type: ignore
import requests  # type: ignore
from rasterio.io import MemoryFile  # type: ignore

from .api_handles import APIObject
from .attrs import ProcessingRequestAttrs
from .constants import Result
from .exceptions import (InvalidRenderingTypeError,
                         PolygonNotReadyForProcessingError, RequestHasNoData)


class ProcessingRequest(APIObject, ProcessingRequestAttrs):
    """Processing request endpoint object"""
    _editable_attrs: set = set()
    _endpoint: str = 'processing_request'
    _allowed_result_types: set = set()

    def refresh(self):
        """Updates the response data of the Processing request.

        Raises:
            InvalidRenderingTypeError: If an already-created processing
                request is a different rendering type than requested.
        """
        super(ProcessingRequest, self).refresh()
        if ('rendering_type' in self._data.keys() and
                self._data['rendering_type'] != self.rendering_type):
            raise InvalidRenderingTypeError(
                self._data['id'],
                self._data['rendering_type'])

    @classmethod
    def create(cls, **kwargs) -> APIObject:
        """Creates Processing request endpoint object.

        Returns:
            APIObject: APIObject instatiated into ProcessingRequest child.
        """
        cls.validate(kwargs)
        kwargs['date_from'], kwargs['date_to'] = \
            ProcessingRequest.correct_dates(
                [kwargs['date_from'],
                 kwargs['date_to']]
            )

        return super(ProcessingRequest, cls).create(**kwargs)

    @classmethod
    def validate(cls, kwargs: dict):
        """Validates Processing request result status.

        Args:
            kwargs (dict)

        Raises:
            PolygonNotReadyForProcessingError: If the Processing request is
                created or requested while the target Polygon is not yet
                processed.
        """
        if 'polygon' in kwargs and not kwargs['polygon'].is_ready():
            raise PolygonNotReadyForProcessingError(kwargs['polygon'].status)

    @staticmethod
    def correct_dates(dates: list) -> list:
        """Checks if dates need to be corrected and does so.

        Args:
            dates (list): Dates within a processing request.

        Returns:
            tuple: List with converted dates.
        """
        return (
            [ProcessingRequest.convert_date_to_str(date)
                if isinstance(date, datetime)
                else date
                for date in dates]
        )

    @staticmethod
    def convert_date_to_str(date: datetime) -> str:
        """Converts datetime.date to string if necessary

        Args:
            date (datetime): Date in datetime.datetime format.

        Returns:
            str: Date in string format.
        """
        try:
            return datetime.strftime(date, "%Y-%m-%d")
        except ValueError:
            raise

    def has_data(self) -> bool:
        """Checks whether the Processing request returned any data.

        Returns:
            bool: Data filling statetment.
        """
        return (
            (self._data['status'] != 'no_data') and
            (self._data['status'] != 'error') and
            ('result' in self._data)
        )


class RasterProcessingRequest(ProcessingRequest):
    """Baseclass for raster and vector Processing request results.
Mainly serves for handlig results."""

    def _get_result_url(self, result_type: Result) -> str:
        """Acquires result URL from the Processing request response
                based on desired result type.

        Args:
            result_type (Result): One of the available result types.
                See https://bit.ly/2Yjg6wk for further information.

        Raises:
            RequestHasNoData: If result has returned no data. This might
                be caused due to unavailability of satellite images within
                the date range.

        Returns:
            str: URL to download/view the result.
        """
        if self.has_data():
            return self._data['result'][result_type.value]
        else:
            raise RequestHasNoData(self.id)

    def _get_content(self, result_type: Result) -> bytes:
        """Acquires the content of the Processing request response.

        Args:
            result_type (Result): One of the available result types
                for the given Processing request. See https://bit.ly/2Yjg6wk
                for further information.

        Returns:
            bytes: Response content as bytes text.
        """
        return requests.get(
            self._get_result_url(result_type),
            allow_redirects=True).content

    def _get_raster(self, result_type: Result) -> np.ndarray:
        """Where applicable, returns raster result as NumPy array.

        Args:
            result_type (Result): One of the available *raster* result types
                for the given Processing request. See https://bit.ly/2Yjg6wk
                for further information.

        Returns:
            numpy.ndarray: Multidimensional NumPy array.
        """
        content = self._get_content(result_type)
        with MemoryFile(content) as memfile:
            with memfile.open() as dataset:
                data_array = dataset.read().astype('float32')
        return data_array

    def _save_raster(self, result_type: Result, path: str):
        """Saves raster result of the Processing request.

        Args:
            result_type (Result): One of the available *raster* result types
                for the given Processing request. See https://bit.ly/2Yjg6wk
                for further information.
            path (str): Path to save the file.
        """
        content = self._get_content(result_type)
        with open(path, 'wb') as dst:
            dst.write(content)

    def _get_vector(self, result_type) -> gpd.GeoDataFrame:
        """Where applicable, returns vector result as Geopandas GeoDataFrame.

        Returns:
            gpd.GeoDataFrame: Geopandas GeoDataFrame.
        """
        content = self._get_content(result_type)
        return gpd.GeoDataFrame.from_features(fiona.BytesCollection(content))

    def as_array(self, clouds_as_nan: bool = True,
                 outwards_as_nan: bool = True) -> np.ndarray:
        """Wrapper method for private _get_raster.

        Args:
            clouds_as_nan (bool): Whether convert clouds to NumPy.nan instead
                of default -999
            outwards_as_nan (bool): Whether convert values outside of the
                field shape to NumPy.nan instead of deafult -998

        Returns:
            numpy.ndarray: Multidimensional NumPy array.
        """
        raw = self._get_raster(Result.RAW)

        if clouds_as_nan:
            raw[raw == -999] = np.nan
        if outwards_as_nan:
            raw[raw == -998] = np.nan

        return raw

    def get_tiff_url(self) -> str:
        """Returns RAW (TIFF) URL.

        Returns:
            str: RAW (TIFF) URL.
        """
        return self._get_result_url(Result.RAW)

    def save_tiff(self, path: str):
        """Saves result in RAW TIFF format.

        Args:
            path (str): Path to save the file.
        """
        self._save_raster(Result.RAW, path)

    def get_colored_tiff_url(self) -> str:
        """Returns COLORED TIFF URL.

        Returns:
            str: COLORED TIFF URL.
        """
        return self._get_result_url(Result.COLOR)

    def save_colored_tiff(self, path: str):
        """Saves result in COLORED TIFF format.

        Args:
            path (str): Path to save the file.
        """
        self._save_raster(Result.COLOR, path)

    def get_png_url(self) -> str:
        """Returns PNG URL.

        Returns:
            str: PNG URL.
        """
        return self._get_result_url(Result.PNG)

    def save_png(self, path: str):
        """Saves result in PNG format.

        Args:
            path (str): Path to save the file.
        """
        self._save_raster(Result.PNG, path)

    def get_tiles_url(self) -> str:
        """Get tiles URL.

        Returns:
            str: Tiles URL.
        """
        return self._get_result_url(Result.TILES_COLOR)

    def get_demo_tiles_url(self) -> str:
        """Get demo tiles URL for preview.

        Returns:
            str: Demo tiles URL.
        """
        return self._get_result_url(Result.TILES_DEMO)

    def preview(self):
        """Opens default browser in a new tab using
                demo tiles URL. This is an easy result preview.
        """
        url = self._get_result_url(Result.TILES_DEMO)
        webbrowser.open(url, new=2)

    def as_geodataframe(self) -> gpd.GeoDataFrame:
        """Wrapper method for private _get_vector.

        Returns:
            gpd.GeoDataFrame: Geopandas GeoDataFrame.
        """
        return self._get_vector(Result.SHP)

    def get_shapefile_url(self) -> str:
        """Returns shapefile URL.

        Returns:
            str: Shapefile URL.
        """
        return self._get_result_url(Result.SHP)

    def save_shapefile(self, path: str):
        """Saves result in as shapefile.

        Args:
            path (str): Path to save the file.
        """
        gdf = self._get_vector(Result.SHP)
        gdf.to_file(path)

    def get_geojson_url(self) -> str:
        """Returns GeoJSON URL.

        Returns:
            str: GeoJSON URL.
        """
        return self._get_result_url(Result.GEOJSON)

    def save_geojson(self, path: str):
        """Saves result as GeoJSON.

        Args:
            path (str): Path to save the file.
        """
        gdf = self._get_vector(Result.GEOJSON)
        gdf.to_file(path, driver='GeoJSON')

    def get_frequencies_url(self) -> str:
        """Returns frequencies URL.

        Returns:
            str: Frequencies URL.
        """
        return self._get_result_url(Result.FREQUENCIES)

    def get_frequencies(self) -> dict:
        """Acquires percentual shares of value intervals
        of the field area.

        Returns:
            dict: Keys are tuples of intervals, values are percentual
                shares.

        """
        freqs_bytes = self._get_content(Result.FREQUENCIES)

        try:
            freqs = json.loads(freqs_bytes.decode('utf-8'))
        except JSONDecodeError:
            raise

        return {eval(k): v for k, v in freqs.items()}


class JSONProcessingRequest(ProcessingRequest):
    """Baseclass for JSON Processing request results.
Mainly serves for handlig results."""
    def get_json(self) -> dict:
        """Acquires JSON result as a dictionary from the Processing request response.

        Raises:
            RequestHasNoData: If result has returned no data. This might
                be caused due to unavailability of satellite images within
                the date range.

        Returns:
            dict: JSON data as Python dictionary.
        """
        if self.has_data():
            return self._data['result']['time_series']
        else:
            raise RequestHasNoData(self.id)

    def save_json(self, path: str):
        """Saves JSON result.

        Args:
            path (str): Path to save the file.
        """
        content = self.get_json()
        with open(path, 'w') as dst:
            json.dump(content, dst)


class ObservationBase(RasterProcessingRequest):
    """Baseclass for specific methods of Observation"""

    def _get_stats(self) -> dict:
        """Acquires descriptive statistics that are always present
        for the Observation endpoint for the current field.
        This method is should not be used itself. It is encapsulated in
        methods regarding particular stats. You can choose from:
        *mean*, *median*, *standard deviation*, *minimum*, *maximum*
        and dictionary of *percentiles*.

        Returns:
            dict: Dictionary of yet unselected statistics.
        """
        stats_bytes = self._get_content(Result.STATISTICS)

        try:
            return json.loads(stats_bytes.decode('utf-8'))
        except JSONDecodeError:
            raise

    def get_stats_url(self) -> str:
        """Returns stats URL.

        Returns:
            str: Stats URL.
        """
        return self._get_result_url(Result.STATISTICS)

    def get_mean(self) -> float:
        """Returns mean of the field from the Observation endpoint.

        Returns:
            float: Mean of the field values.
        """
        return self._get_stats()['mean']

    def get_median(self) -> float:
        """Returns median of the field from the Observation endpoint.

        Returns:
            float: Median of the field values.
        """
        return self._get_stats()['median']

    def get_sd(self) -> float:
        """Returns standard deviation of the field from the Observation endpoint.

        Returns:
            float: Standard deviation of the field values.
        """
        return self._get_stats()['sd']

    def get_min(self) -> float:
        """Returns minimum of the field from the Observation endpoint.

        Returns:
            float: Minimum of the field values.
        """
        return self._get_stats()['min']

    def get_max(self) -> float:
        """Returns maximum of the field from the Observation endpoint.

        Returns:
            float: Maximum of the field values.
        """
        return self._get_stats()['max']

    def get_percentiles(self) -> dict:
        """Returns percentiles of the field from the Observation endpoint.

        Returns:
            float: Percentiles of the field values.
        """
        return self._get_stats()['percentiles']


class FieldZonationBase(RasterProcessingRequest):
    """Baseclass for specific methods of FieldZonation"""
    def get_simplified_geojson_url(self) -> str:
        """Returns simplified GeoJSON URL.

        Returns:
            str: Simplified GeoJSON URL.
        """
        return self._get_result_url(Result.GEOJSON_SIMPLIFIED)

    def save_simplified_geojson(self, path: str):
        """Saves simplified GeoJSON result.

        Args:
            path (str): Path to save the file.
        """
        gdf = self._get_vector(Result.GEOJSON_SIMPLIFIED)
        gdf.to_file(path, driver='GeoJSON')

    def get_simplified_shapefile_url(self) -> str:
        """Returns simplified shapefile URL.

        Returns:
            str: Simplified shapefile URL.
        """
        return self._get_result_url(Result.SHP_SIMPLIFIED)

    def save_simplified_shapefile(self, path: str):
        """Saves simplified shapefile result.

        Args:
            path (str): Path to save the file.
        """
        gdf = self._get_vector(Result.SHP_SIMPLIFIED)
        gdf.to_file(path)
