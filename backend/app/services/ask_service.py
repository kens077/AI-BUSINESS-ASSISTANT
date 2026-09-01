
from sqlalchemy.orm import Session

from app.services.context_service import get_business_context
from app.services.ai_service import generate_answer


def answer_business_question(
    db: Session,
    business_id: int,
    question: str,
) -> str:

    context = get_business_context(
        db=db,
        business_id=business_id,
    )

    if context == "Business not found.":
        return context

    answer = generate_answer(
        question=question,
        context=context,
    )

    return answer

