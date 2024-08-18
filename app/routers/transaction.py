from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import models, schema
from app.database import get_db
from app.routers.oauth2 import get_current_user

router = APIRouter(
    prefix="/categories/{cid}/transactions",
    tags=["Transactions"]
)

# Create a transaction
@router.post("/", response_model=schema.TransactionResponse)
def create_transaction(cid: int, transaction: schema.TransactionCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    category = db.query(models.Category).filter(models.Category.id == cid, models.Category.user_id == user.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db_transaction = models.Transaction(
        amount=transaction.amount,
        note=transaction.note,
        transactionDate=transaction.transactionDate,  
        category_id=cid,
        user_id=user.id  
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Get all transactions for a category
@router.get("/", response_model=List[schema.TransactionResponse])
def get_transactions(cid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    transactions = db.query(models.Transaction).filter(models.Transaction.category_id == cid, models.Transaction.user_id == user.id).all()
    return transactions

# Get a specific transaction by ID
@router.get("/{tid}", response_model=schema.TransactionResponse)
def get_transaction(cid: int, tid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == tid, models.Transaction.category_id == cid, models.Transaction.user_id == user.id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction

# Update a transaction
@router.put("/{tid}", response_model=schema.TransactionResponse)
def update_transaction(cid: int, tid: int, transaction: schema.TransactionCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == tid, models.Transaction.category_id == cid, models.Transaction.user_id == user.id).first()
    if not db_transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    # Update transaction fields
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    
    
    db_transaction.user_id = user.id
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

# Delete a transaction
@router.delete("/{tid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(cid: int, tid: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == tid, models.Transaction.category_id == cid, models.Transaction.user_id == user.id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return None