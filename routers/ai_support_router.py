from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from database import get_db
from dependencies import get_current_user
from models import AIChatLog, User

router = APIRouter(prefix="/api/ai-support", tags=["AI Support"])


# -----------------------------
# Request model
# -----------------------------
class AIMessage(BaseModel):
    message: str


# -----------------------------
# AI Logic
# -----------------------------
def get_ai_response(message: str):

    msg = message.lower().replace(" ", "")

    if "createpost" in msg or "addpost" in msg or "newpost" in msg:
        return "To create a post, go to My Posts → Click 'Create Post' and fill in title and content."

    elif "editpost" in msg or "updatepost" in msg or "edit" in msg:
        return "Go to My Posts → Click Edit on the post you want to update."

    elif "deletepost" in msg or "removepost" in msg or "delete" in msg:
        return "Open your post in My Posts and click the Delete button."

    elif "subscription" in msg or "plan" in msg or "upgrade" in msg:
        return "You can subscribe by visiting the Subscription page and selecting a plan."

    elif "billing" in msg or "invoice" in msg or "payment" in msg:
        return "Billing history and invoices are available in your subscription dashboard."

    elif "profile" in msg or "editprofile" in msg:
        return "You can edit your profile from the Profile page."

    elif "dashboard" in msg or "stats" in msg:
        return "Dashboard shows analytics like total posts, comments and likes."

    elif "likes" in msg:
        return "You can see all likes on your posts in the Likes section."

    elif "comments" in msg:
        return "You can manage and reply to comments from the Comments page."

    else:
        return "I'm here to help! You can ask about posts, subscriptions, billing, profile, comments, or likes."


# -----------------------------
# AI Support API
# -----------------------------
@router.post("/")
def ai_support(
    data: Optional[AIMessage] = None,
    message: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    # Accept both body or query
    if data:
        user_message = data.message
    elif message:
        user_message = message
    else:
        return {"error": "Message is required"}

    ai_response = get_ai_response(user_message)

    # Save chat log
    log = AIChatLog(
        user_id=current_user.id,
        question=user_message,
        answer=ai_response
    )

    db.add(log)
    db.commit()

    return {
        "question": user_message,
        "answer": ai_response
    }