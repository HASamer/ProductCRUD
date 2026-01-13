from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from .ProductEntity import Product

def create_product(db: Session, name: str, quantity: str, category: str) -> Product:
    product = Product(name=name, quantity=quantity, category=category)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_product(db: Session, product_id: uuid.UUID) -> Optional[Product]:
    return db.query(Product).filter(Product.id == product_id).first()

def list_products(db: Session, limit: int = 100) -> List[Product]:
    return db.query(Product).limit(limit).all()

def update_product(db: Session, product_id: uuid.UUID, **kwargs) -> Optional[Product]:
    product = get_product(db, product_id)
    if not product:
        return None
    for k, v in kwargs.items():
        if v is not None and hasattr(product, k):
            setattr(product, k, v)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, product_id: uuid.UUID) -> bool:
    product = get_product(db, product_id)
    if not product:
        return False
    db.delete(product)
    db.commit()
    return True