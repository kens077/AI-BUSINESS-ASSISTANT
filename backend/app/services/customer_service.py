
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate


def create_customer(
    db: Session,
    customer_data: CustomerCreate
) -> Customer:

    # Check that the business exists
    business = db.query(Business).filter(
        Business.id == customer_data.business_id
    ).first()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    customer = Customer(
        business_id=customer_data.business_id,
        name=customer_data.name,
        email=customer_data.email,
        phone=customer_data.phone,
    )

    db.add(customer)
    db.commit()
    db.refresh(customer)

    return customer


def get_customers(db: Session) -> list[Customer]:
    return db.query(Customer).all()
