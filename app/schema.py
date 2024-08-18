from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserResponseWithToken(UserResponse):
    access_token: str
    token_type: str
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    email: str
    password: str

class CategoryBase(BaseModel):
    title: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True        

class TransactionBase(BaseModel):
    amount: float
    note: Optional[str] = None
    transactionDate: datetime

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    category_id: int

    class Config:
        from_attributes = True