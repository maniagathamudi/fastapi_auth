# services/notification_service.py

from datetime import datetime
from services.email_service import send_email


async def notify_post_owner(post, acting_user, activity_type: str):

    subject = f"New {activity_type} on your post"

    body = f"""
Post: "{post.title}"
User: {acting_user.email}
Activity: {activity_type} on your post
Time: {datetime.utcnow().strftime("%Y-%m-%d %I:%M %p")}
"""

    await send_email(
        subject=subject,
        body=body,
        recipient=post.author.email if hasattr(post, "author") else None
    )