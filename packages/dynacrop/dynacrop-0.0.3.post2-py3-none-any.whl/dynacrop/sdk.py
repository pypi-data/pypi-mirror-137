from __future__ import annotations

from typing import Any, Iterable, Optional, Set

from geopandas import GeoDataFrame  # type: ignore
from shapely import wkt  # type: ignore

from .api_handles import APIObject
from .attrs import PolygonAttrs, UserAttrs
from .constants import Layer
from .processing_request_base import (FieldZonationBase, JSONProcessingRequest,
                                      ObservationBase)


class User(APIObject, UserAttrs):
    """User endpoint object"""
    _editable_attrs: Set[Any] = set()
    _endpoint: str = 'user'

    def __init__(self):
        """Creates User endpoint object"""
        super(User, self).__init__()

    def __repr__(self) -> str:
        """Prints information about the user.

        Returns:
            str: The information.
        """
        return str(self.__dict__['_data'])


class Polygon(APIObject, PolygonAttrs):
    """Polygon endpoint object"""
    _editable_attrs: Set[Any] = {
        'max_mean_cloud_cover',
        'label',
        'smi_enabled'}
    _endpoint: str = 'polygons'

    @classmethod
    def create(cls,  # type: ignore
               geometry: str,
               label: Optional[str] = None,
               max_mean_cloud_cover: Optional[int] = None,
               smi_enabled: bool = False, **kwargs) -> Polygon:  # type: ignore
        """Creates Polygon endpoint object.

        Args:
            geometry (str): Valid polygon shape in
                Well Known Text (WKT) representation
                (see: https://en.wikipedia.org/wiki/Well-\
                    known_text_representation_of_geometry).
            label (Optional[str], optional): Description to the Polygon
                (user field). Defaults to None.
            max_mean_cloud_cover (Optional[int], optional): Maximum mean cloud
                coverage in decimal percentage (i.e. 0.3). Defaults to None.
            smi_enabled (bool, optional): To enable Soil Moisture Index
                pre-computation. Defaults to False.

        Returns:
            Polygon: APIObject instantiated into Polygon child.
        """
        return super(Polygon, cls).create(
                geometry=geometry,
                label=label,
                max_mean_cloud_cover=max_mean_cloud_cover,
                smi_enabled=smi_enabled)  # type: ignore

    @staticmethod
    def as_geodataframe(
        polygons: list,
        fields: list = [
            "id",
            "area",
            "last_valid_observation",
            "smi_enabled",
            "max_mean_cloud_cover",
            "label",
            "valid_observations",
            "cloud_cover_percent",
            "last_updated",
            "created_date",
            "completed_date",
            "last_updated"
        ],
        iterables_to_strings: Optional[bool] = True
    ) -> GeoDataFrame:
        """Create a Geopandas GeoDataFrame from a list of Polygon objects. This
        can be then saved to a file by GeoDataFrame `to_file` method.

        Args:
            polygons (list): A list of polygons to create the GeoDataFrame
                from.
            fields (Optional[list], optional): Polygon attributes that will be
                represented as fields in the GeoDataFrame. Iterable attributes
                are converted to string for save . Defaults to ["id", "area",
                "last_valid_observation", "smi_enabled", "max_mean_cloud_cover"
                , "label", "valid_observations", "cloud_cover_percent",
                "last_updated", "created_date", "completed_date", "last_updated
                "].
            iterables_to_strings (Optional[bool], optional): If True, all
                iterable Polygon attributes will be converted to strings
                for saving purposes. Spatial files usually reject saving Python
                iterables to attribute tables.

        Returns:
            GeoDataFrame: GeoDataFrame of polygons.
        """
        data = [[getattr(p, field) for field in fields] for p in polygons]

        if iterables_to_strings:
            data = [[str(attr) if isinstance(attr, Iterable) else attr
                     for attr in attrs] for attrs in data]

        geometry = [wkt.loads(p.geometry) for p in polygons]
        return GeoDataFrame(
            data=data,
            geometry=geometry,
            columns=fields
        )


class TimeSeries(JSONProcessingRequest):
    """Time series endpoint object. Time series is the service of
DynaCrop API."""
    rendering_type = 'time_series'

    @classmethod
    def create(cls,  # type: ignore
               polygon: Polygon,
               layer: Layer,
               date_from: str,
               date_to: str) -> TimeSeries:
        """Creates Time series endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://dynacrop.worldfromspace.cz/docs/#/products
                for further information.
            date_from (str): Date to record time series from.
            date_to (str): Date to record time series to.

        Returns:
            APIObject: APIObject instatiated into TimeSeries child.
        """
        return super(TimeSeries, cls).create(polygon_id=polygon.id,
                                             rendering_type=cls.rendering_type,
                                             layer=layer.value,
                                             date_from=date_from,
                                             date_to=date_to)  # type: ignore


class Observation(ObservationBase):
    """Observation endpoint object. Observation is the service of
DynaCrop API."""
    rendering_type = 'observation'

    @classmethod
    def create(cls,  # type: ignore
               polygon: Polygon,
               layer: Layer,
               date_from: str,
               date_to: str) -> Observation:  # type: ignore
        """Creates Observation endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://dynacrop.worldfromspace.cz/docs/#/products
                for further information.
            date_from (str): Date to watch for observation from.
            date_to (str): Date to watch for observation to.

        Returns:
            APIObject: APIObject instatiated into Observation child.
        """
        return super(Observation, cls). \
            create(
                polygon_id=polygon.id,
                rendering_type=cls.rendering_type,
                layer=layer.value,
                date_from=date_from,
                date_to=date_to)  # type: ignore


class FieldZonation(FieldZonationBase):
    """Field zonation endpoint object. Field zonation is the service of
    DynaCrop API."""
    rendering_type = 'field_zonation'

    @classmethod
    def create(cls,  # type: ignore
               polygon: Polygon,
               layer: Layer,
               date_from: str,
               date_to: str,
               number_of_zones: int = 3) -> FieldZonation:  # type: ignore
        """Creates Field zonation endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://dynacrop.worldfromspace.cz/docs/#/products
                for further information.
            date_from (str): Date to compute field zonation from.
            date_to (str): Date to compute field zonation to.
            number_of_zones (int): Number of zones to separate the field to.
                The number of zones must be one of 3, 5, 10, 20, 255.

        Returns:
            APIObject: APIObject instatiated into FieldZonation child.
        """
        return super(FieldZonation, cls). \
            create(
                polygon_id=polygon.id,
                rendering_type=cls.rendering_type,
                layer=layer.value,
                date_from=date_from,
                date_to=date_to,
                number_of_zones=str(number_of_zones))  # type: ignore


class FieldZonationByMedian(FieldZonationBase):
    """Field zonation by median endpoint object. Field zonation by median
is the service of DynaCrop API."""
    rendering_type = 'field_zonation_by_median'

    @classmethod
    def create(cls,  # type: ignore
               polygon: Polygon,
               layer: Layer,
               date_from: str,
               date_to: str,
               thresholds: Optional[list] = None) \
            -> FieldZonationByMedian:  # type: ignore
        """Creates Field zonation by median endpoint object.

        Args:
            polygon (Polygon): Polygon endpoint object.
            layer (str): Should be Layer enumration. One of the DynaCrop API
                layers. See https://dynacrop.worldfromspace.cz/docs/#/products
                for further information.
            date_from (str): Date to compute field zonation by median from.
            date_to (str): Date to compute field zonation by median to.
            thresholds (list): Thresholds to zone the field in between.
                The number of thresholds must be one of 2, 4, 9, 19, 254.

        Returns:
            APIObject: APIObject instatiated into FieldZonationByMedian child.
        """
        return super(FieldZonationByMedian, cls).\
            create(
                polygon_id=polygon.id,
                rendering_type=cls.rendering_type,
                layer=layer.value,
                date_from=date_from,
                date_to=date_to,
                thresholds=thresholds)  # type: ignore
