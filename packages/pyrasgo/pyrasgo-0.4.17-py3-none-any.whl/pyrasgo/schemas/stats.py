from pydantic import BaseModel
from typing import Optional


class GenerateStat(BaseModel):
    dwTableId: int
    dimensionColumnId: Optional[int]
    onlyIfDataChanged: Optional[bool]