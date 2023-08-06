from typing import List, Dict

from pydantic import BaseModel

from model.model.report.column import Column


class Dataset(BaseModel):
    columns: List[Column] = None
    results: Dict = {}
