from typing import Optional
from pydantic import BaseModel, Field

class PortalBaseModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    slug: str = Field(..., min_length=1, max_length=100)
    base_url: str = Field(..., min_length=1, max_length=500)
    query: dict = Field({},)
    web: str = Field(..., min_length=1, max_length=100)

class PortalModel(PortalBaseModel):
    id: str

class PortalDetailModel(PortalModel):
    retrieve_data_url: str

class PortalUpdateModel(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    base_url: Optional[str] = None
    query: Optional[dict] = None
    web: Optional[str] = None