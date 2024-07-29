from pydantic import BaseModel, Field

class ItemModel(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=500)
    price: float = Field(..., gt=0)

class ItemDB(ItemModel):
    id: str
