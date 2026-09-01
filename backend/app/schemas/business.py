from pydantic import BaseModel


class BusinessCreate(BaseModel):
    name: str
    industry: str
    description: str | None = None


class BusinessResponse(BaseModel):
    id: int
    name: str
    industry: str
    description: str | None = None

    model_config = {
        "from_attributes": True
    }
