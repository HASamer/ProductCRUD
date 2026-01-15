from typing import List, Optional
import uuid
from sqlalchemy.orm import Session
from prometheus_client import Counter
from .ProductModel import (
    create_product as _create,
    get_product as _get,
    list_products as _list,
    update_product as _update,
    delete_product as _delete,
)
from .ProductEntity import Product

# Domain-specific Prometheus counters for product operations
PRODUCT_CREATE_TOTAL = Counter(
    "product_create_total",
    "Total number of successfully created products",
)
PRODUCT_READ_TOTAL = Counter(
    "product_read_total",
    "Total number of successfully read products by id",
)
PRODUCT_LIST_TOTAL = Counter(
    "product_list_total",
    "Total number of successful product list operations",
)
PRODUCT_UPDATE_TOTAL = Counter(
    "product_update_total",
    "Total number of successfully updated products",
)
PRODUCT_DELETE_TOTAL = Counter(
    "product_delete_total",
    "Total number of successfully deleted products",
)


def create_product(db: Session, name: str, quantity: str, category: str) -> Product:
    product = _create(db, name=name, quantity=quantity, category=category)
    PRODUCT_CREATE_TOTAL.inc()
    return product


def get_product(db: Session, product_id: str) -> Optional[Product]:
    try:
        pid = uuid.UUID(product_id)
    except (ValueError, TypeError):
        return None
    product = _get(db, pid)
    if product is not None:
        PRODUCT_READ_TOTAL.inc()
    return product


def list_products(db: Session, limit: int = 100) -> List[Product]:
    products = _list(db, limit=limit)
    PRODUCT_LIST_TOTAL.inc()
    return products


def update_product(db: Session, product_id: str, **fields) -> Optional[Product]:
    try:
        pid = uuid.UUID(product_id)
    except (ValueError, TypeError):
        return None
    updated = _update(db, pid, **fields)
    if updated is not None:
        PRODUCT_UPDATE_TOTAL.inc()
    return updated


def delete_product(db: Session, product_id: str) -> bool:
    try:
        pid = uuid.UUID(product_id)
    except (ValueError, TypeError):
        return False
    ok = _delete(db, pid)
    if ok:
        PRODUCT_DELETE_TOTAL.inc()
    return ok
