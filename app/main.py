from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import user, category, transaction
from .database import engine
from . import models

# Create the FastAPI app
app = FastAPI()

# Allow CORS for development purposes (adjust as needed)
origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
# Include routers
app.include_router(user.router)
app.include_router(category.router)
app.include_router(transaction.router)

# Create the database tables
models.Base.metadata.create_all(bind=engine)


#welcome page

@app.get("/")
def main_page():
    return {"message": "Welcome to the FastAPI Expense Tracker!"}