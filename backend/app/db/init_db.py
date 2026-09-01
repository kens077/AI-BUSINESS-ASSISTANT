from app.db.database import Base, engine

# Import all models so SQLAlchemy knows about them
from app.models.business import Business
from app.models.customer import Customer
from app.models.product import Product
from app.models.sale import Sale


print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
