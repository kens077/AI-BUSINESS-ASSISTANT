from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class Business(Base):
    __tablename__ = "businesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    industry = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)

    customers = relationship("Customer", back_populates="business")
    products = relationship("Product", back_populates="business")
    sales = relationship("Sale", back_populates="business")
