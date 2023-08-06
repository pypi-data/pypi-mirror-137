from pydantic import BaseModel

from model.model.pipeline.trigger_type import TriggerType


class TriggerData(BaseModel):
    topicName: str = None
    triggerType: TriggerType = None
    data: dict = None
