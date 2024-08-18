import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from app.routers import oauth2
from app import models, schema, utils
from app.database import get_db
from app.config import settings  

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register/", response_model=schema.Token)
async def register_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    logger.debug("Register user endpoint called with email: %s", user.email)
    
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        logger.warning("Email already registered: %s", user.email)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    hashed_password = utils.get_password_hash(user.password)
    new_user = models.User(
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=hashed_password  
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = oauth2.create_access_token(
        data={"user_id": new_user.id},
        expires_delta=access_token_expires
    )
    
    logger.info("User registered and JWT token created for user id: %s", new_user.id)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/login/", response_model=schema.Token)
def login(login_data: schema.LoginData, db: Session = Depends(get_db)):
    logger.debug("Login attempt with email: %s", login_data.email)
    
    user = db.query(models.User).filter(models.User.email == login_data.email).first()
    
    if not user or not utils.verify_password(login_data.password, user.password):
        logger.warning("Invalid credentials for email: %s", login_data.email)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = oauth2.create_access_token(
        data={"user_id": user.id},
        expires_delta=access_token_expires
    )
    
    logger.info("User logged in and JWT token created for user id: %s", user.id)
    return {"access_token": access_token, "token_type": "bearer"}