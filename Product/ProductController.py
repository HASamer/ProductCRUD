
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from typing import List, Optional
from sqlalchemy.orm import Session
from DatabaseCore import SessionLocal
from .ProductService import (
    create_product as svc_create,
    get_product as svc_get,
    list_products as svc_list,
    update_product as svc_update,
    delete_product as svc_delete,
)

router = APIRouter(prefix="/products", tags=["products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str
    quantity: str
    category: str

class ProductRead(BaseModel):
    id: str
    name: str
    quantity: str
    category: str

    class Config:
        orm_mode = True

    @field_validator("id", mode="before")
    def convert_id_to_str(self, value):
        return str(value)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    quantity: Optional[str] = None
    category: Optional[str] = None

@router.post("/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create(p: ProductCreate, db: Session = Depends(get_db)):
    created = svc_create(db, p.name, p.quantity, p.category)
    return created

@router.get("/", response_model=List[ProductRead])
def list_all(limit: int = 100, db: Session = Depends(get_db)):
    return svc_list(db, limit=limit)

@router.get("/{product_id}", response_model=ProductRead)
def read(product_id: str, db: Session = Depends(get_db)):
    prod = svc_get(db, product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="Product not found")
    return prod

@router.put("/{product_id}", response_model=ProductRead)
def update(product_id: str, payload: ProductUpdate, db: Session = Depends(get_db)):
    updated = svc_update(db, product_id, **payload.dict())
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found or invalid id")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove(product_id: str, db: Session = Depends(get_db)):
    ok = svc_delete(db, product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found or invalid id")
    return None
