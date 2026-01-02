from datetime import datetime

from pydantic import BaseModel


class EventEnvelope(BaseModel):
    event_id: str
    event_type: str
    occurred_at: datetime
    payload: dict
    trace_id: str | None = None
