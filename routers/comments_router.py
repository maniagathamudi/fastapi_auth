from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import get_db
from models import Post, Comment, User, Notification
from dependencies import get_current_user
from services.notification_service import notify_post_owner

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.post("/{post_id}")
def add_comment(
    post_id: int,
    content: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_comment = Comment(
        content=content,
        post_id=post_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(post)

    # 🔔 Save notification
    if post.author_id != current_user.id:
        notification = Notification(
            user_id=post.author_id,
            message=f"{current_user.email} commented on your post '{post.title}' 💬",
            type="comment"
        )

        db.add(notification)
        db.commit()

    background_tasks.add_task(
        notify_post_owner,
        post,
        current_user,
        "commented on"
    )

    return {"message": "Comment added successfully."}


@router.get("/")
def get_comments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    comments = db.query(Comment).filter(
        Comment.user_id == current_user.id
    ).all()

    return comments