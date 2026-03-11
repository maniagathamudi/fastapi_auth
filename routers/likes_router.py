from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Post, Like, User, UserSubscription, Notification
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

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=403,
            detail="Please subscribe to a plan first."
        )

    if subscription.end_date and subscription.end_date < datetime.utcnow():
        raise HTTPException(
            status_code=403,
            detail="Your subscription has expired. Please renew your plan."
        )

    plan = subscription.plan

    existing_like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == current_user.id
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="You have already liked this post.")

    user_like_count = db.query(Like).filter(
        Like.user_id == current_user.id
    ).count()

    if plan.like_limit != -1 and user_like_count >= plan.like_limit:
        raise HTTPException(
            status_code=403,
            detail="You’ve reached your plan limit. Kindly upgrade your plan to continue."
        )

    new_like = Like(
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_like)
    db.commit()
    db.refresh(post)

    # 🔔 Save notification for post owner
    if post.author_id != current_user.id:
        notification = Notification(
            user_id=post.author_id,
            message=f"{current_user.email} liked your post '{post.title}' 👍",
            type="like"
        )

        db.add(notification)
        db.commit()

    # Email notification
    background_tasks.add_task(
        notify_post_owner,
        post,
        current_user,
        "liked"
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