from pydantic import BaseModel, AnyUrl
from typing import Optional


class LivePredictEventData(BaseModel):
    request_type: str
    endpoint_id: str
    model_type: str
    image_url: AnyUrl
    image_id: str
    webhooks: str
