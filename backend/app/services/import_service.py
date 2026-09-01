import pandas as pd
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale


REQUIRED_COLUMNS = {
    "customer_name",
    "customer_email",
    "product_name",
    "category",
    "quantity",
    "unit_price",
}


def import_business_file(
    db: Session,
    business_id: int,
    file_path: str,
):
    # Check business
    business = db.query(Business).filter(
        Business.id == business_id
    ).first()

    if not business:
        raise ValueError("Business not found.")

    # Read Excel or CSV
    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)

    # Clean column names
    df.columns = [
        str(column).strip().lower().replace(" ", "_")
        for column in df.columns
    ]

    missing_columns = REQUIRED_COLUMNS - set(df.columns)

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )

    imported_sales = 0

    for _, row in df.iterrows():

        customer_name = str(
            row["customer_name"]
        ).strip()

        customer_email = str(
            row["customer_email"]
        ).strip()

        product_name = str(
            row["product_name"]
        ).strip()

        category = str(
            row["category"]
        ).strip()

        quantity = int(row["quantity"])
        unit_price = float(row["unit_price"])

        if not customer_name:
            continue

        if not product_name:
            continue

        if quantity <= 0:
            continue

        if unit_price < 0:
            continue

        # -------------------------
        # Customer
        # -------------------------

        customer = db.query(Customer).filter(
            Customer.business_id == business_id,
            Customer.email == customer_email,
        ).first()

        if not customer:

            customer = Customer(
                business_id=business_id,
                name=customer_name,
                email=customer_email,
            )

            db.add(customer)
            db.flush()

        # -------------------------
        # Product
        # -------------------------

        product = db.query(Product).filter(
            Product.business_id == business_id,
            Product.name == product_name,
        ).first()

        if not product:

            product = Product(
                business_id=business_id,
                name=product_name,
                category=category,
                description="Imported from business data",
                price=unit_price,
            )

            db.add(product)
            db.flush()

        # -------------------------
        # Sale
        # -------------------------

        total_amount = quantity * unit_price

        sale = Sale(
            business_id=business_id,
            customer_id=customer.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=unit_price,
            total_amount=total_amount,
        )

        db.add(sale)

        imported_sales += 1

    db.commit()

    return {
        "message": "Business data imported successfully.",
        "rows_imported": imported_sales,
    }