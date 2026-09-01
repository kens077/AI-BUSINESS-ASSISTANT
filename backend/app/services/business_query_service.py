from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale


def get_business_metrics(
    db: Session,
    business_id: int,
):
    customers = (
        db.query(Customer)
        .filter(Customer.business_id == business_id)
        .all()
    )

    products = (
        db.query(Product)
        .filter(Product.business_id == business_id)
        .all()
    )

    sales = (
        db.query(Sale)
        .filter(Sale.business_id == business_id)
        .all()
    )

    total_revenue = sum(
        float(sale.total_amount or 0)
        for sale in sales
    )

    return {
        "business_id": business_id,
        "customer_count": len(customers),
        "product_count": len(products),
        "total_sales": len(sales),
        "total_revenue": total_revenue,
    }


# -------------------------
# Sales Analytics
# -------------------------

def get_business_analytics(
    db: Session,
    business_id: int,
):
    sales = (
        db.query(Sale)
        .filter(Sale.business_id == business_id)
        .all()
    )

    products = (
        db.query(Product)
        .filter(Product.business_id == business_id)
        .all()
    )

    customers = (
        db.query(Customer)
        .filter(Customer.business_id == business_id)
        .all()
    )

    # -------------------------
    # Basic Analytics
    # -------------------------

    total_sales = len(sales)

    total_revenue = sum(
        float(sale.total_amount or 0)
        for sale in sales
    )

    total_quantity_sold = sum(
        int(sale.quantity or 0)
        for sale in sales
    )

    average_sale_value = (
        total_revenue / total_sales
        if total_sales > 0
        else 0
    )


    # -------------------------
    # Product Analytics
    # -------------------------

    product_map = {
        product.id: product
        for product in products
    }

    product_stats = {}

    for sale in sales:

        product = product_map.get(
            sale.product_id
        )

        if not product:
            continue

        product_id = product.id

        if product_id not in product_stats:

            product_stats[product_id] = {
                "product_id": product_id,
                "product_name": product.name,
                "quantity_sold": 0,
                "revenue": 0,
            }

        product_stats[product_id][
            "quantity_sold"
        ] += int(sale.quantity or 0)

        product_stats[product_id][
            "revenue"
        ] += float(sale.total_amount or 0)


    top_products = sorted(
        product_stats.values(),
        key=lambda product: product["revenue"],
        reverse=True,
    )


    # -------------------------
    # Customer Analytics
    # -------------------------

    customer_map = {
        customer.id: customer
        for customer in customers
    }

    customer_stats = {}

    for sale in sales:

        customer = customer_map.get(
            sale.customer_id
        )

        if not customer:
            continue

        customer_id = customer.id

        if customer_id not in customer_stats:

            customer_stats[customer_id] = {
                "customer_id": customer_id,
                "customer_name": customer.name,
                "purchase_count": 0,
                "revenue": 0,
            }

        customer_stats[customer_id][
            "purchase_count"
        ] += 1

        customer_stats[customer_id][
            "revenue"
        ] += float(sale.total_amount or 0)


    top_customers = sorted(
        customer_stats.values(),
        key=lambda customer: customer["revenue"],
        reverse=True,
    )


    # -------------------------
    # Final Analytics Response
    # -------------------------

    return {
        "business_id": business_id,

        "total_sales": total_sales,

        "total_revenue": total_revenue,

        "total_quantity_sold":
            total_quantity_sold,

        "average_sale_value":
            average_sale_value,

        "top_products":
            top_products,

        "top_customers":
            top_customers,
    }