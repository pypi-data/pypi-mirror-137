from enum import Enum
from typing import List

from model.model.common.watchmen_model import WatchmenModel
from model.model.topic.factor import Factor


class TopicType(Enum):
    RAW = "raw",
    DISTINCT = "distinct",
    AGGREGATE = "aggregate",
    TIME = "time",
    RATIO = "ratio",
    NOT_DEFINED = "not-defined",
    SYSTEM = "system"


class Topic(WatchmenModel):
    topicId: str = None
    name: str = None
    # code: str = None
    type: str = None
    kind: str = None
    factors: List[Factor] = []
    description: str = None
    tenantId: str = None
    dataSourceId: str = None

    # factorIds: list = []
