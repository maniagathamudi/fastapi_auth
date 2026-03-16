import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query
from sqlalchemy.orm import Session
from typing import Optional

import models, schemas
from dependencies import get_db, get_current_user


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

UPLOAD_DIR = "media/posts"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# CREATE POST WITH IMAGE
from datetime import datetime

@router.post("/", response_model=schemas.PostResponse)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    publish_option: str = Form("publish"),  # publish | draft | schedule
    scheduled_at: Optional[str] = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    status = "published"
    publish_time = None

    # -------------------------
    # DRAFT
    # -------------------------
    if publish_option == "draft":
        status = "draft"

    # -------------------------
    # SCHEDULE
    # -------------------------
    elif publish_option == "schedule":

        if not scheduled_at:
            raise HTTPException(status_code=400, detail="scheduled_at required")

        publish_time = datetime.fromisoformat(scheduled_at)

        if publish_time <= datetime.utcnow():
            raise HTTPException(status_code=400, detail="scheduled_at must be future")

        status = "scheduled"

    # -------------------------
    # IMAGE UPLOAD
    # -------------------------
    image_path = None

    if image:

        file_location = f"{UPLOAD_DIR}/{image.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = file_location

    # -------------------------
    # CREATE POST
    # -------------------------
    new_post = models.Post(

        title=title,
        content=content,
        image=image_path,

        status=status,
        scheduled_at=publish_time,

        published_at=datetime.utcnow() if status == "published" else None,

        author_id=current_user.id
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
# GET POSTS WITH PAGINATION + SEARCH
@router.get("/")
def get_posts(
    page: int = Query(1),
    limit: int = Query(10),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):

    query = db.query(models.Post)

    if search:
        query = query.filter(
            models.Post.title.contains(search) |
            models.Post.content.contains(search)
        )

    total = query.count()

    posts = query.offset((page - 1) * limit).limit(limit).all()

    results = []

    for post in posts:

        image_url = None

        if post.image:
            image_url = f"http://127.0.0.1:8000/{post.image}"

        results.append({
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "image": image_url,
            "author_id": post.author_id
        })

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
        "data": results
    }


# GET SINGLE POST
@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


# DELETE POST
@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(post)
    db.commit()

    return {"message": "Post deleted"}