from sqlalchemy.orm import Session

from app.services.business_query_service import get_business_metrics


def get_business_insights(
    db: Session,
    business_id: int,
):
    metrics = get_business_metrics(
        db=db,
        business_id=business_id,
    )

    customer_count = metrics["customer_count"]
    product_count = metrics["product_count"]
    total_sales = metrics["total_sales"]
    total_revenue = metrics["total_revenue"]

    insights = []

    # -------------------------
    # Revenue & Sales Insights
    # -------------------------

    if total_sales == 0:
        insights.append(
            "No sales have been recorded yet. "
            "Start recording sales to track business revenue."
        )
    else:
        insights.append(
            f"The business has generated ₹{total_revenue:,.2f} "
            f"from {total_sales} recorded sale(s)."
        )

        average_sale = total_revenue / total_sales

        insights.append(
            f"The average revenue per sale is "
            f"₹{average_sale:,.2f}."
        )

    # -------------------------
    # Customer Insights
    # -------------------------

    if customer_count == 0:
        insights.append(
            "There are currently no customers in the system. "
            "Adding customer data will help track customer growth."
        )
    else:
        insights.append(
            f"The business currently has "
            f"{customer_count} customer(s)."
        )

    # -------------------------
    # Product Insights
    # -------------------------

    if product_count == 0:
        insights.append(
            "No products have been added to the catalog yet."
        )
    else:
        insights.append(
            f"The product catalog currently contains "
            f"{product_count} product(s)."
        )

    # -------------------------
    # Revenue Opportunity
    # -------------------------

    if customer_count > 0 and total_sales == 0:
        insights.append(
            "Customers are available but no sales have been recorded. "
            "Converting existing customers into sales could increase revenue."
        )

    # -------------------------
    # Overall Business Status
    # -------------------------

    if total_revenue > 0 and customer_count > 0 and product_count > 0:
        insights.append(
            "The business has customers, products, and recorded sales, "
            "providing a basic foundation for tracking business performance."
        )

    return {
        "business_id": business_id,
        "insights": insights,
    }
