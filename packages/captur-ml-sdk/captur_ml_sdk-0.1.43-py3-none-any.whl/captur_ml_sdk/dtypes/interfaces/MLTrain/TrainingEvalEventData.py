from pydantic import BaseModel


class TrainingEvalEventData(BaseModel):
    model_id: str
    request_type: str
