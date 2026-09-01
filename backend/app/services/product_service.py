
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(
    db: Session,
    product_data: ProductCreate
) -> Product:

    # Check that the business exists
    business = db.query(Business).filter(
        Business.id == product_data.business_id
    ).first()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    # Check that the price is not negative
    if product_data.price < 0:
        raise HTTPException(
            status_code=400,
            detail="Product price cannot be negative"
        )

    product = Product(
        business_id=product_data.business_id,
        name=product_data.name,
        category=product_data.category,
        description=product_data.description,
        price=product_data.price,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session) -> list[Product]:
    return db.query(Product).all()
