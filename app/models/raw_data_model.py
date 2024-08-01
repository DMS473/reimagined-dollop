from typing import Optional
from pydantic import BaseModel, Field

class RawDataBaseModel(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)

class RawDataModel(RawDataBaseModel):
    id: str