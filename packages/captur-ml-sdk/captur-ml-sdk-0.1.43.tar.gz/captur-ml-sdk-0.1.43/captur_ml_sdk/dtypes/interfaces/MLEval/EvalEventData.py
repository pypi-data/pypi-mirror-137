from captur_ml_sdk.dtypes.generics import Image, Meta
from pydantic import BaseModel
from typing import List, Optional

class EvalEventData(BaseModel):
    request_id: str
    meta: Optional[Meta]
    images: List[Image]
    model_name: str
    model_id: str
    model_type: str
