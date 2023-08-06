from enum import Enum

from pydantic import BaseModel


class Join(BaseModel):
    topicId: str = None
    factorId: str = None
    type: str = None
    secondaryTopicId: str = None
    secondaryFactorId: str = None


class JoinType(str, Enum):
    inner = "inner"
    left = "left"
    right = "right"
