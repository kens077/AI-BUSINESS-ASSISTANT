from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale


def get_business_summary(
    db: Session,
    business_id: int
):
    # Customer count
    customer_count = db.query(Customer).filter(
        Customer.business_id == business_id
    ).count()

    # Product count
    product_count = db.query(Product).filter(
        Product.business_id == business_id
    ).count()

    # Total sales
    total_sales = db.query(Sale).filter(
        Sale.business_id == business_id
    ).count()

    # Total revenue
    total_revenue = db.query(
        func.coalesce(func.sum(Sale.total_amount), 0)
    ).filter(
        Sale.business_id == business_id
    ).scalar()

    # Average sale value
    average_sale_value = db.query(
        func.coalesce(func.avg(Sale.total_amount), 0)
    ).filter(
        Sale.business_id == business_id
    ).scalar()

    # Total quantity sold
    total_quantity_sold = db.query(
        func.coalesce(func.sum(Sale.quantity), 0)
    ).filter(
        Sale.business_id == business_id
    ).scalar()

    return {
        "business_id": business_id,
        "customer_count": customer_count,
        "product_count": product_count,
        "total_sales": total_sales,
        "total_revenue": float(total_revenue),
        "average_sale_value": float(average_sale_value),
        "total_quantity_sold": int(total_quantity_sold),
    }