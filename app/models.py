from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, Text, func
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    created_at = Column(DateTime, default=func.now())

    categories = relationship("Category", back_populates="owner")
    transactions = relationship("Transaction", back_populates="owner")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="categories")
    transactions = relationship("Transaction", back_populates="category")

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    note = Column(Text)
    transactionDate = Column(DateTime, default=datetime.utcnow)
    category_id = Column(Integer, ForeignKey("categories.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    category = relationship("Category", back_populates="transactions")
    owner = relationship("User", back_populates="transactions")