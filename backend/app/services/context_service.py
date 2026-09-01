from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale


def get_business_context(
    db: Session,
    business_id: int,
) -> str:

    # -------------------------
    # Get Business
    # -------------------------

    business = db.query(Business).filter(
        Business.id == business_id
    ).first()

    if not business:
        return "Business not found."


    # -------------------------
    # Basic Metrics
    # -------------------------

    customer_count = db.query(
        func.count(Customer.id)
    ).filter(
        Customer.business_id == business_id
    ).scalar()


    product_count = db.query(
        func.count(Product.id)
    ).filter(
        Product.business_id == business_id
    ).scalar()


    total_sales = db.query(
        func.count(Sale.id)
    ).filter(
        Sale.business_id == business_id
    ).scalar()


    total_revenue = db.query(
        func.coalesce(func.sum(Sale.total_amount), 0)
    ).filter(
        Sale.business_id == business_id
    ).scalar()


    total_quantity_sold = db.query(
        func.coalesce(func.sum(Sale.quantity), 0)
    ).filter(
        Sale.business_id == business_id
    ).scalar()


    # -------------------------
    # Average Sale Value
    # -------------------------

    if total_sales and total_sales > 0:

        average_sale_value = (
            float(total_revenue) / total_sales
        )

    else:

        average_sale_value = 0


    # -------------------------
    # Product Analytics
    # -------------------------

    product_analytics = (
        db.query(
            Product.id,
            Product.name,
            func.coalesce(
                func.sum(Sale.quantity),
                0
            ).label("quantity_sold"),
            func.coalesce(
                func.sum(Sale.total_amount),
                0
            ).label("revenue"),
        )
        .outerjoin(
            Sale,
            Sale.product_id == Product.id
        )
        .filter(
            Product.business_id == business_id
        )
        .group_by(
            Product.id,
            Product.name
        )
        .order_by(
            func.coalesce(
                func.sum(Sale.total_amount),
                0
            ).desc()
        )
        .all()
    )


    product_lines = []

    for product in product_analytics:

        product_lines.append(
            f"- {product.name}: "
            f"quantity sold={int(product.quantity_sold)}, "
            f"revenue=₹{float(product.revenue):,.2f}"
        )


    products_text = "\n".join(
        product_lines
    )


    # -------------------------
    # Customer Analytics
    # -------------------------

    customer_analytics = (
        db.query(
            Customer.id,
            Customer.name,
            func.count(Sale.id).label(
                "purchase_count"
            ),
            func.coalesce(
                func.sum(Sale.total_amount),
                0
            ).label("revenue"),
        )
        .outerjoin(
            Sale,
            Sale.customer_id == Customer.id
        )
        .filter(
            Customer.business_id == business_id
        )
        .group_by(
            Customer.id,
            Customer.name
        )
        .order_by(
            func.coalesce(
                func.sum(Sale.total_amount),
                0
            ).desc()
        )
        .all()
    )


    customer_lines = []

    for customer in customer_analytics:

        customer_lines.append(
            f"- {customer.name}: "
            f"purchases={int(customer.purchase_count)}, "
            f"revenue=₹{float(customer.revenue):,.2f}"
        )


    customers_text = "\n".join(
        customer_lines
    )


    # -------------------------
    # Product Catalog
    # -------------------------

    products = db.query(Product).filter(
        Product.business_id == business_id
    ).all()


    catalog_lines = []

    for product in products:

        catalog_lines.append(
            f"- {product.name}: "
            f"category={product.category}, "
            f"price=₹{float(product.price):,.2f}"
        )


    catalog_text = "\n".join(
        catalog_lines
    )


    # -------------------------
    # Final AI Context
    # -------------------------

    return f"""
Business:
Name: {business.name}
Industry: {business.industry}
Description: {business.description or "N/A"}

Business Metrics:
Customers: {customer_count}
Products: {product_count}
Total Sales: {total_sales}
Total Revenue: ₹{float(total_revenue):,.2f}
Total Quantity Sold: {int(total_quantity_sold)}
Average Sale Value: ₹{average_sale_value:,.2f}

Product Performance:
{products_text or "No product sales available."}

Customer Performance:
{customers_text or "No customer sales available."}

Product Catalog:
{catalog_text or "No products available."}
""".strip()