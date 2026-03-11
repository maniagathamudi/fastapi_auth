from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

import os

# Database
from database import Base, engine, get_db, SessionLocal

# Models & Schemas
from models import User, SubscriptionPlan
from schemas import UserCreate, UserResponse, UserUpdate, ChangePassword

# Auth
from auth import create_access_token
from dependencies import get_current_user

# Email service
from services.email_service import send_email

# Routers
from routers.likes_router import router as likes_router
from routers.posts_router import router as posts_router
from routers.comments_router import router as comments_router
from routers.subscription_router import router as subscription_router
from routers.notification_router import router as notification_router
from routers.ai_support_router import router as ai_support_router


# -------------------------
# Password hashing
# -------------------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# -------------------------
# Create database tables
# -------------------------
Base.metadata.create_all(bind=engine)


# -------------------------
# Create FastAPI app
# -------------------------
app = FastAPI(
    title="FastAPI Blog API",
    version="2.1.0"
)


# =====================================================
# CORS (React frontend support)
# =====================================================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================
# Ensure media folder exists
# =====================================================
os.makedirs("media/invoices", exist_ok=True)


# -------------------------
# Static media
# -------------------------
app.mount("/media", StaticFiles(directory="media"), name="media")


# =====================================================
# CREATE DEFAULT PLANS
# =====================================================
def create_default_plans():

    db = SessionLocal()

    try:
        existing = db.query(SubscriptionPlan).count()

        if existing == 0:

            plans = [

                SubscriptionPlan(
                    name="Basic",
                    price=199,
                    post_limit=1,
                    image_limit=1,
                    like_limit=5,
                    comment_limit=5
                ),

                SubscriptionPlan(
                    name="Premium",
                    price=499,
                    post_limit=2,
                    image_limit=2,
                    like_limit=20,
                    comment_limit=20
                ),

                SubscriptionPlan(
                    name="Pro",
                    price=999,
                    post_limit=9999,
                    image_limit=9999,
                    like_limit=9999,
                    comment_limit=9999
                ),
            ]

            db.add_all(plans)
            db.commit()

    finally:
        db.close()


@app.on_event("startup")
def startup_event():
    create_default_plans()


# =====================================================
# INCLUDE ROUTERS
# =====================================================
app.include_router(likes_router)
app.include_router(posts_router)
app.include_router(comments_router)
app.include_router(subscription_router)
app.include_router(notification_router)
app.include_router(ai_support_router)


# =====================================================
# AUTHENTICATION
# =====================================================

# -------------------------
# Signup
# -------------------------
@app.post("/signup")
def signup(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        hashed_password=pwd_context.hash(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    background_tasks.add_task(
        send_email,
        subject="Welcome to FastAPI Blog 🎉",
        recipient=new_user.email,
        body=f"Hello {new_user.first_name},\n\nWelcome to our Blog Platform!"
    )

    return {"message": "User created successfully"}


# -------------------------
# Signin
# -------------------------
@app.post("/signin")
def signin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(User.email == form_data.username).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid email")

    if not pwd_context.verify(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    token = create_access_token({"user_id": db_user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


# =====================================================
# USER PROFILE
# =====================================================

@app.get("/profile", response_model=UserResponse)
def profile(current_user: User = Depends(get_current_user)):
    return current_user


@app.put("/edit-profile")
def edit_profile(
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    current_user.first_name = data.first_name
    current_user.last_name = data.last_name

    db.commit()
    db.refresh(current_user)

    return {"message": "Profile updated successfully"}


@app.put("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if not pwd_context.verify(data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Old password incorrect")

    current_user.hashed_password = pwd_context.hash(data.new_password)

    db.commit()

    return {"message": "Password changed successfully"}


@app.delete("/delete-account")
def delete_account(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    db.delete(current_user)
    db.commit()

    return {"message": "Account deleted successfully"}


# =====================================================
# EMAIL TEST
# =====================================================
@app.get("/test-email")
def test_email(background_tasks: BackgroundTasks):

    background_tasks.add_task(
        send_email,
        subject="Test Email",
        recipient="your_test_email@example.com",
        body="This is a test email from FastAPI."
    )

    return {"message": "Email triggered successfully"}


# =====================================================
# ROOT
# =====================================================
@app.get("/")
def root():
    return {"message": "API working successfully 🚀"}