from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import models, schema
from app.database import get_db
from app.routers.oauth2 import get_current_user  

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[schema.CategoryResponse])
def get_categories(
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    categories = db.query(models.Category).filter(models.Category.user_id == user.id).all()
    return categories

@router.get("/{id}", response_model=schema.CategoryResponse)
def get_category(
    id: int, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    category = db.query(models.Category).filter(models.Category.id == id, models.Category.user_id == user.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

@router.post("/", response_model=schema.CategoryResponse)
def create_category(
    category: schema.CategoryCreate, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    db_category = models.Category(**category.dict(), user_id=user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.put("/{id}", response_model=schema.CategoryResponse)
def update_category(
    id: int, 
    category: schema.CategoryCreate, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    db_category = db.query(models.Category).filter(models.Category.id == id, models.Category.user_id == user.id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    for key, value in category.dict().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

@router.delete("/{id}")
def delete_category(
    id: int, 
    db: Session = Depends(get_db), 
    user: models.User = Depends(get_current_user)
):
    db_category = db.query(models.Category).filter(models.Category.id == id, models.Category.user_id == user.id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db.delete(db_category)
    db.commit()
    return {"message": "Category deleted successfully"}