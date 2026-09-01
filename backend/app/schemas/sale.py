from pydantic import BaseModel


class SaleCreate(BaseModel):
    business_id: int
    customer_id: int
    product_id: int
    quantity: int


class SaleResponse(BaseModel):
    id: int
    business_id: int
    customer_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_amount: float

    model_config = {
        "from_attributes": True
    }
