from pydantic import BaseModel, Field
from typing import Optional

class termBaseModel(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    data: dict = Field({},)
    species: str = Field(..., min_length=1, max_length=100)

class TermModel(termBaseModel):
    id: str

class ListOfParams(BaseModel):
    species: list = []

class searchParams(BaseModel):
    search: str = Field(..., min_length=1, max_length=500)