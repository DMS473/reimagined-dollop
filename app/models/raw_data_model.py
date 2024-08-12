from pydantic import BaseModel, Field
from typing import Optional

class RawDataBaseModel(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    data: dict = Field({},)
    web: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., min_length=1, max_length=100)

class RawDataModel(RawDataBaseModel):
    id: str

class ListOfParams(BaseModel):
    species: Optional[list[str]] = None
    web: Optional[list[str]] = None