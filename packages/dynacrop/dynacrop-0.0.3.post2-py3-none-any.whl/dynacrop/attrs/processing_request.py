
from typing import Optional

from ..constants import Layer
from .async_request import AsyncRequestAttrs


class ProcessingRequestAttrs(AsyncRequestAttrs):
    date_from: str
    date_to: str
    value_no_data: int
    value_clouds: int
    result: dict
    layer: Layer
    polygon_id: int
    number_of_zones: Optional[int]
    thresholds: list
