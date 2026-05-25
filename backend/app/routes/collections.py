from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.collection import Collection
from app.models.product import Product
from app.models.user import User
from app.routes.auth import get_current_user
from app.schemas.collection import CollectionCreate, CollectionResponse
from typing import List

router = APIRouter(prefix="/collections", tags=["collections"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("", response_model=List[CollectionResponse])
def get_collections(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Collection).filter(Collection.user_email == current_user.email).all()

@router.post("", response_model=CollectionResponse)
def create_collection(data: CollectionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    collection = Collection(name=data.name, user_email=current_user.email)
    db.add(collection)
    db.commit()
    db.refresh(collection)
    return collection

@router.delete("/{collection_id}")
def delete_collection(collection_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    collection = db.query(Collection).filter(Collection.id == collection_id, Collection.user_email == current_user.email).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Products referencing this collection will automatically have collection_id set to NULL due to ON DELETE SET NULL
    db.delete(collection)
    db.commit()
    return {"status": "deleted"}

@router.post("/{collection_id}/products/{product_id}")
def add_product_to_collection(collection_id: int, product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    collection = db.query(Collection).filter(Collection.id == collection_id, Collection.user_email == current_user.email).first()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
        
    product = db.query(Product).filter(Product.id == product_id, Product.alert_user_email == current_user.email).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found or not owned by you")
        
    product.collection_id = collection.id
    db.commit()
    return {"status": "added to collection"}
