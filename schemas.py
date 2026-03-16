from pydantic import BaseModel, EmailStr
from typing import Optional


# USER SCHEMAS (unchanged)
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    first_name: str
    last_name: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


# -------------------------
# UPDATED POST RESPONSE
# -------------------------
class PostResponse(BaseModel):

    id: int
    title: str
    content: str
    image: Optional[str]
    author_id: int

    class Config:
        from_attributes = True


# COMMENT
class CommentCreate(BaseModel):
    content: str


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    post_id: int

    class Config:
        from_attributes = True


# LIKE
class LikeResponse(BaseModel):
    id: int
    user_id: int
    post_id: int

    class Config:
        from_attributes = True

from datetime import datetime

# -------------------------
# CREATE POST
# -------------------------
class PostCreate(BaseModel):

    title: str
    content: str
    scheduled_at: Optional[datetime] = None


# -------------------------
# UPDATED POST RESPONSE
# -------------------------
class PostResponse(BaseModel):

    id: int
    title: str
    content: str
    image: Optional[str]

    status: str
    scheduled_at: Optional[datetime]
    published_at: Optional[datetime]

    author_id: int

    class Config:
        from_attributes = True        