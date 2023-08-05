from typing import Optional


class AsyncRequestAttrs:
    id: int
    status: str
    error: Optional[str]
    completed_date: str
    created_date: str
    rendering_time: int
