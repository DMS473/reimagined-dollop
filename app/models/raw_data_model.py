from pydantic import BaseModel, Field

class RawDataBaseModel(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    data: dict = Field({},)
    web: str = Field(..., min_length=1, max_length=100)
    species: str = Field(..., min_length=1, max_length=100)

class RawDataModel(RawDataBaseModel):
    id: str

class ListOfSpecies(BaseModel):
    species: list