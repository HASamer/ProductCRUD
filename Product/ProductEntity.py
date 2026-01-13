import uuid

from sqlalchemy import Column, String, Text, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from DatabaseCore import Base

class Product(Base):
    __tablename__ = "Products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    category = Column(String, nullable=False)

    def __repr__(self):
        return f"<Product(id='{self.id}', Category='{self.category}', Product name='{self.name}', Quantity='{self.quantity}')>"