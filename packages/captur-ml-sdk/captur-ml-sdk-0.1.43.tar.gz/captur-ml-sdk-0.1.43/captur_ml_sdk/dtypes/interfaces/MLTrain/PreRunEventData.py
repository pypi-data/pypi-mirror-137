from pydantic import (
    BaseModel,
    HttpUrl, root_validator
)

from typing import Optional, List

from captur_ml_sdk.dtypes.generics import Image, TrainingMeta
from captur_ml_sdk.dtypes.interfaces.validators import check_images_or_imagefile_has_data


class PreRunEventData(BaseModel):
    request_id: str
    meta: Optional[TrainingMeta]
    images: Optional[List[Image]]
    imagesfile: Optional[str]
    model_name: str
    base_model_id: str
    include_data: Optional[str]
    exclude_classes: Optional[List[str]]
    base_dataset_id: str

    root_validator(check_images_or_imagefile_has_data)
