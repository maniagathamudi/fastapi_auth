import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form, Query
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
# CREATE POST WITH IMAGE
@router.post("/", response_model=schemas.PostResponse)
def create_post(
    title: str = Form(...),
    content: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):

    # 1️⃣ Check subscription
    subscription = db.query(models.UserSubscription).filter(
        models.UserSubscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Please subscribe to a plan first."
        )

    plan = subscription.plan

    # 2️⃣ Check POST LIMIT (handle unlimited = -1)
    user_post_count = db.query(models.Post).filter(
        models.Post.author_id == current_user.id
    ).count()

    if plan.post_limit != -1 and user_post_count >= plan.post_limit:
        raise HTTPException(
            status_code=403,
            detail="Post limit reached. Upgrade your plan."
        )

    # 3️⃣ Check IMAGE LIMIT (only if image uploaded)
    image_path = None

    if image:

        user_image_count = db.query(models.Post).filter(
            models.Post.author_id == current_user.id,
            models.Post.image != None
        ).count()

        if plan.image_limit != -1 and user_image_count >= plan.image_limit:
            raise HTTPException(
                status_code=403,
                detail="Image upload limit reached. Upgrade your plan."
            )

        file_location = f"{UPLOAD_DIR}/{image.filename}"

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = file_location

    # 4️⃣ Create post
    new_post = models.Post(
        title=title,
        content=content,
        image=image_path,
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