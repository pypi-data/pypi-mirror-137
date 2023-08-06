from typing import List

from model.model.common.watchmen_model import WatchmenModel
from model.model.pipeline.pipeline import Pipeline


class PipelineFlow(WatchmenModel):
    topicId: str = None
    consume: List[Pipeline]
    produce: List[Pipeline]
    tenantId: str = None
