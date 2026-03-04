from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from dependencies import get_db

router = APIRouter(prefix="/auth")


@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    hashed = auth.hash_password(user.password)

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter(
        models.User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(401)

    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(401)

    token = auth.create_token(db_user.id)

    return {"access_token": token}