from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Post, Like, User, UserSubscription
from dependencies import get_current_user
from services.notification_service import notify_post_owner

router = APIRouter(prefix="/likes", tags=["Likes"])


@router.post("/{post_id}")
def like_post(
    post_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # 1️⃣ Check if post exists
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # 2️⃣ Check active subscription
    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Please subscribe to a plan first."
        )

    # 3️⃣ Check subscription expiry
    if subscription.end_date and subscription.end_date < datetime.utcnow():
        raise HTTPException(
            status_code=403,
            detail="Your subscription has expired. Please renew your plan."
        )

    plan = subscription.plan

    # 4️⃣ Prevent duplicate likes
    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="You have already liked this post.")

    # 5️⃣ Check like limit (unlimited = -1)
    user_like_count = db.query(Like).filter(
        Like.user_id == current_user.id
    ).count()

    if plan.like_limit != -1 and user_like_count >= plan.like_limit:
        raise HTTPException(
            status_code=403,
            detail="You’ve reached your plan limit. Kindly upgrade your plan to continue."
        )

    # 6️⃣ Create like
    new_like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_like)
    db.commit()
    db.refresh(post)

    # 7️⃣ Trigger Email Notification
    background_tasks.add_task(
        notify_post_owner,
        post,
        current_user,
        "Like"
    )

    return {"message": "Post liked successfully."}

@router.get("/")
def get_likes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    likes = db.query(Like).filter(
        Like.user_id == current_user.id
    ).all()

    return likes