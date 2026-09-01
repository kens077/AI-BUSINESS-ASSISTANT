
from app.db.database import SessionLocal

from app.models.business import Business
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale


def seed_data():
    db = SessionLocal()

    try:
        # Get the existing business
        business = db.query(Business).filter(
            Business.name == "ABC Paints"
        ).first()

        # Create the business only if it doesn't exist
        if not business:
            business = Business(
                name="ABC Paints",
                industry="Paint Manufacturing",
                description="Paint and coating manufacturer",
            )

            db.add(business)
            db.commit()
            db.refresh(business)

            print("Business created.")

        else:
            print(f"Using existing business: {business.name} (ID: {business.id})")

        # -------------------------
        # Customer
        # -------------------------

        customer = db.query(Customer).filter(
            Customer.business_id == business.id
        ).first()

        if not customer:
            customer = Customer(
                business_id=business.id,
                name="Rahul Sharma",
                email="rahul@example.com",
                phone="9876543210",
            )

            db.add(customer)
            db.commit()
            db.refresh(customer)

            print("Customer created.")
        else:
            print(f"Using existing customer: {customer.name}")

        # -------------------------
        # Products
        # -------------------------

        interior_paint = db.query(Product).filter(
            Product.business_id == business.id,
            Product.name == "Premium Interior Paint"
        ).first()

        if not interior_paint:
            interior_paint = Product(
                business_id=business.id,
                name="Premium Interior Paint",
                category="Interior Paint",
                description="High-quality interior wall paint",
                price=2499.0,
            )

            db.add(interior_paint)
            db.commit()
            db.refresh(interior_paint)

            print("Interior paint created.")
        else:
            print("Interior paint already exists.")

        exterior_paint = db.query(Product).filter(
            Product.business_id == business.id,
            Product.name == "Premium Exterior Paint"
        ).first()

        if not exterior_paint:
            exterior_paint = Product(
                business_id=business.id,
                name="Premium Exterior Paint",
                category="Exterior Paint",
                description="Weather-resistant exterior paint",
                price=2999.0,
            )

            db.add(exterior_paint)
            db.commit()
            db.refresh(exterior_paint)

            print("Exterior paint created.")
        else:
            print("Exterior paint already exists.")

        # -------------------------
        # Sale
        # -------------------------

        sale = db.query(Sale).filter(
            Sale.business_id == business.id
        ).first()

        if not sale:
            sale = Sale(
                business_id=business.id,
                customer_id=customer.id,
                product_id=interior_paint.id,
                quantity=2,
                unit_price=2499.0,
                total_amount=4998.0,
            )

            db.add(sale)
            db.commit()
            db.refresh(sale)

            print("Sale created.")
        else:
            print("Sale already exists.")

        print()
        print("Sample data setup complete!")
        print(f"Business ID: {business.id}")
        print(f"Customer ID: {customer.id}")
        print(f"Product IDs: {interior_paint.id}, {exterior_paint.id}")
        print(f"Sale ID: {sale.id}")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
