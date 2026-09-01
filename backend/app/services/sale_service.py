from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale
from app.schemas.sale import SaleCreate


def create_sale(
    db: Session,
    sale_data: SaleCreate
) -> Sale:

    # Check that the business exists
    business = db.query(Business).filter(
        Business.id == sale_data.business_id
    ).first()

    if not business:
        raise HTTPException(
            status_code=404,
            detail="Business not found"
        )

    # Check that the customer exists
    customer = db.query(Customer).filter(
        Customer.id == sale_data.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    # Check that the customer belongs to the business
    if customer.business_id != sale_data.business_id:
        raise HTTPException(
            status_code=400,
            detail="Customer does not belong to this business"
        )

    # Check that the product exists
    product = db.query(Product).filter(
        Product.id == sale_data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Check that the product belongs to the business
    if product.business_id != sale_data.business_id:
        raise HTTPException(
            status_code=400,
            detail="Product does not belong to this business"
        )

    # Validate quantity
    if sale_data.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0"
        )

    # Get price directly from the product
    unit_price = float(product.price)

    # Calculate total sale amount
    total_amount = sale_data.quantity * unit_price

    # Create sale
    sale = Sale(
        business_id=sale_data.business_id,
        customer_id=sale_data.customer_id,
        product_id=sale_data.product_id,
        quantity=sale_data.quantity,
        unit_price=unit_price,
        total_amount=total_amount,
    )

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale


def get_sales(db: Session) -> list[Sale]:
    return db.query(Sale).all()