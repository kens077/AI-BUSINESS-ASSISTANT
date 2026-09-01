from pydantic import BaseModel


class ProductCreate(BaseModel):
    business_id: int
    name: str
    category: str | None = None
    description: str | None = None
    price: float


class ProductResponse(BaseModel):
    id: int
    business_id: int
    name: str
    category: str | None = None
    description: str | None = None
    price: float

    model_config = {
        "from_attributes": True
    }
