from pydantic import BaseModel, Field
from typing import Optional

class RawDataBaseModel(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    data: dict = Field({},)
    web: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., min_length=1, max_length=100)

class RawDataModel(RawDataBaseModel):
    id: str

class ListOfSpecies(BaseModel):
    species: list

class ListOfParams(BaseModel):
    species: Optional[list] = None
    web: Optional[list] = None