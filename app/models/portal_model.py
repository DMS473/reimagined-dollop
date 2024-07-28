from pydantic import BaseModel, Field

class PortalModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    base_url: str = Field(..., min_length=1, max_length=500)
    query: dict = Field({},)

class PortalDB(PortalModel):
    id: str
