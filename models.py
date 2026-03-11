from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, DateTime, Float, Text
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# =========================================================
# USER MODEL
# =========================================================
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # Relationships
    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")

    subscription = relationship(
        "UserSubscription",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    billing_history = relationship(
        "BillingHistory",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================================================
# POST MODEL
# =========================================================
class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    image = Column(String, nullable=True)

    author_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="post", cascade="all, delete-orphan")


# =========================================================
# COMMENT MODEL
# =========================================================
class Comment(Base):

    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")


# =========================================================
# LIKE MODEL
# =========================================================
class Like(Base):

    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="unique_user_post_like"),
    )

    user = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")


# =========================================================
# SUBSCRIPTION PLAN MODEL
# =========================================================
class SubscriptionPlan(Base):

    __tablename__ = "subscription_plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    price = Column(Float, nullable=False)

    post_limit = Column(Integer, nullable=False)
    image_limit = Column(Integer, nullable=False)
    like_limit = Column(Integer, nullable=False)
    comment_limit = Column(Integer, nullable=False)

    subscriptions = relationship("UserSubscription", back_populates="plan", cascade="all, delete-orphan")
    billing_records = relationship("BillingHistory", back_populates="plan", cascade="all, delete-orphan")


# =========================================================
# USER SUBSCRIPTION MODEL
# =========================================================
class UserSubscription(Base):

    __tablename__ = "user_subscriptions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id", ondelete="CASCADE"), nullable=False)

    start_date = Column(DateTime, default=datetime.utcnow)
    end_date = Column(DateTime, nullable=True)

    user = relationship("User", back_populates="subscription")
    plan = relationship("SubscriptionPlan", back_populates="subscriptions")


# =========================================================
# BILLING HISTORY MODEL
# =========================================================
class BillingHistory(Base):

    __tablename__ = "billing_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id", ondelete="CASCADE"), nullable=False)

    transaction_id = Column(String, nullable=False)
    invoice_path = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="billing_history")
    plan = relationship("SubscriptionPlan", back_populates="billing_records")


# =========================================================
# NOTIFICATION MODEL
# =========================================================
class Notification(Base):

    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    message = Column(String, nullable=False)

    type = Column(String, nullable=False)

    is_read = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


# =========================================================
# AI SUPPORT CHAT MODEL
# =========================================================
class AIChatLog(Base):

    __tablename__ = "ai_chat_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    question = Column(Text)

    answer = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)