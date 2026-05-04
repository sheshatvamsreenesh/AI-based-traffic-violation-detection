from sqlalchemy import Column, Integer, String
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)  # "police" or "user"


class Challan(Base):
    __tablename__ = "challans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    violation_type = Column(String(50))
    amount = Column(Integer)
    status = Column(String(20))  # "unpaid" or "paid"
-----------------------------------------------------
from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    role: str   # "police" or "user"


class UserLogin(BaseModel):
    username: str
    password: str


class ChallanResponse(BaseModel):
    id: int
    violation_type: str
    amount: int
    status: str

    class Config:
        orm_mode = True
----------------------------------------------------
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🔹 SIGN UP
@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    # 🔒 Constraint 1: role must be valid
    if user.role not in ["police", "user"]:
        return {"error": "Role must be 'police' or 'user'"}

    # 🔒 Constraint 2: username required
    if not user.username or not user.password:
        return {"error": "Username and password required"}

    # 🔒 Constraint 3: unique username
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        return {"error": "Username already exists"}

    new_user = User(
        username=user.username,
        password=user.password,
        role=user.role
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created successfully"}


# 🔹 LOGIN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    # 🔒 Constraint 4: correct credentials
    if not db_user or db_user.password != user.password:
        return {"error": "Invalid username or password"}

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "role": db_user.role
    }
------------------------------------------------------
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Challan

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 👤 USER: Get own challans
@router.get("/my-challans/{user_id}")
def get_my_challans(user_id: int, db: Session = Depends(get_db)):
    return db.query(Challan).filter(Challan.user_id == user_id).all()


# 💳 USER: Pay challan (dummy)
@router.post("/pay/{challan_id}")
def pay_challan(challan_id: int, db: Session = Depends(get_db)):
    challan = db.query(Challan).filter(Challan.id == challan_id).first()

    if not challan:
        return {"error": "Challan not found"}

    challan.status = "paid"
    db.commit()

    return {"message": "Payment successful (dummy)"}


# 👮 POLICE: View all challans
@router.get("/all-challans")
def get_all_challans(db: Session = Depends(get_db)):
    return db.query(Challan).all()
----------------------------------------------------------
from fastapi import FastAPI
from database import Base, engine
from routes import auth, challan

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(challan.router)


@app.get("/")
def root():
    return {"message": "Backend Running"}
