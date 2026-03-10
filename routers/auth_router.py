from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from dependencies import get_db

router = APIRouter(prefix="/auth")


# REGISTER
@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # check if email already exists
    existing_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}


# LOGIN
@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    # LOGIN USING EMAIL
    db_user = db.query(models.User).filter(
        models.User.email == user.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # verify password
    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # create token
    token = auth.create_token(db_user.id)

    return {
        "access_token": token,
        "token_type": "bearer"
    }