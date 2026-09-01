from pydantic import BaseModel


class AskRequest(BaseModel):
    business_id: int
    question: str


class AskResponse(BaseModel):
    answer: str
