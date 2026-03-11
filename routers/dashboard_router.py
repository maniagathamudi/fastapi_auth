from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Post, Comment, Like, User, Notification
from dependencies import get_current_user


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


# =========================================================
# DASHBOARD DATA
# =========================================================
@router.get("/")
def get_dashboard_data(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Total posts created by user
    total_posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).count()

    # Total comments made by user
    total_comments = db.query(Comment).filter(
        Comment.user_id == current_user.id
    ).count()

    # Total likes received on user's posts
    total_likes = (
        db.query(Like)
        .join(Post, Post.id == Like.post_id)
        .filter(Post.author_id == current_user.id)
        .count()
    )

    posts = db.query(Post).filter(
        Post.author_id == current_user.id
    ).all()

    likes_per_post = []

    for post in posts:
        like_count = db.query(Like).filter(
            Like.post_id == post.id
        ).count()

        likes_per_post.append({
            "post_title": post.title,
            "likes": like_count
        })

    return {
        "total_posts": total_posts,
        "total_comments": total_comments,
        "total_likes": total_likes,
        "likes_per_post": likes_per_post
    }


# =========================================================
# GET USER NOTIFICATIONS
# =========================================================
@router.get("/notifications")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(
        Notification.created_at.desc()
    ).all()

    return notifications


# =========================================================
# UNREAD NOTIFICATION COUNT (FOR BELL BADGE)
# =========================================================
@router.get("/notifications/unread-count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    count = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == 0
    ).count()

    return {"unread_count": count}


# =========================================================
# MARK ALL NOTIFICATIONS AS READ
# =========================================================
@router.put("/notifications/read-all")
def mark_all_notifications_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).all()

    for notification in notifications:
        notification.is_read = 1

    db.commit()

    return {"message": "All notifications marked as read"}