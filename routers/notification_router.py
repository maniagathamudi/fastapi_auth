from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Notification, User
from dependencies import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# ==========================================
# Get All Notifications
# ==========================================
@router.get("/")
def get_notifications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id
    ).order_by(Notification.created_at.desc()).all()

    return notifications


# ==========================================
# Mark All Notifications as Read
# ==========================================
@router.put("/mark-read")
def mark_all_read(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    notifications = db.query(Notification).filter(
        Notification.user_id == current_user.id,
        Notification.is_read == 0
    ).all()

    for n in notifications:
        n.is_read = 1

    db.commit()

    return {"message": "All notifications marked as read"}