from datetime import datetime
from database import SessionLocal
from models import Notification
from services.email_service import send_email


async def notify_post_owner(post, acting_user, activity_type: str):

    db = SessionLocal()

    message = f"{acting_user.email} {activity_type} your post '{post.title}'"

    notification = Notification(
        user_id=post.author_id,
        message=message,
        type=activity_type
    )

    db.add(notification)
    db.commit()

    db.close()

    subject = f"New {activity_type} on your post"

    body = f"""
Post: "{post.title}"
User: {acting_user.email}
Activity: {activity_type}
Time: {datetime.utcnow().strftime("%Y-%m-%d %I:%M %p")}
"""

    await send_email(
        subject=subject,
        body=body,
        recipient=post.author.email if hasattr(post, "author") else None
    )