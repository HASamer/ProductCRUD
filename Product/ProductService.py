
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from .ProductModel import (
    create_product as _create,
    get_product as _get,
    list_products as _list,
    update_product as _update,
    delete_product as _delete,
)
from .ProductEntity import Product

def create_product(db: Session, name: str, quantity: str, category: str) -> Product:
    return _create(db, name=name, quantity=quantity, category=category)

def get_product(db: Session, product_id: str) -> Optional[Product]:
    try:
        pid = uuid.UUID(product_id)
    except (ValueError, TypeError):
        return None
    return _get(db, pid)

def list_products(db: Session, limit: int = 100) -> List[Product]:
    return _list(db, limit=limit)

def update_product(db: Session, product_id: str, **fields) -> Optional[Product]:
    try:
        pid = uuid.UUID(product_id)
    except (ValueError, TypeError):
        return None
    return _update(db, pid, **fields)

def delete_product(db: Session, product_id: str) -> bool:
    try:
        pid = uuid.UUID(product_id)
    except (ValueError, TypeError):
        return False
    return _delete(db, pid)
