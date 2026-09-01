from pydantic import BaseModel


class CustomerCreate(BaseModel):
    business_id: int
    name: str
    email: str | None = None
    phone: str | None = None


class CustomerResponse(BaseModel):
    id: int
    business_id: int
    name: str
    email: str | None = None
    phone: str | None = None

    model_config = {
        "from_attributes": True
    }
