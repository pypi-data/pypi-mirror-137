from .async_request import AsyncRequestAttrs


class PolygonAttrs(AsyncRequestAttrs):
    geometry: str
    area: int
    last_valid_observation: str
    smi_enabled: bool
    max_mean_cloud_cover: float
    label: str
    valid_observations: list
    cloud_cover_percent: list
    last_updated: str
