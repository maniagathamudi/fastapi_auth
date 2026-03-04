from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database import get_db
from models import SubscriptionPlan, UserSubscription, BillingHistory, User
from dependencies import get_current_user
from invoice_utils import generate_invoice


router = APIRouter(prefix="/subscription", tags=["Subscription"])


# =========================================================
# Subscribe / Upgrade Plan
# =========================================================
@router.post("/subscribe/{plan_id}")
def subscribe(
    plan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # 1️⃣ Check if plan exists
    plan = db.query(SubscriptionPlan).filter(
        SubscriptionPlan.id == plan_id
    ).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    # 2️⃣ Check existing subscription
    existing_subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == current_user.id
    ).first()

    start_date = datetime.utcnow()
    end_date = start_date + timedelta(days=30)

    # 3️⃣ If already subscribed → Upgrade / Renew
    if existing_subscription:
        existing_subscription.plan_id = plan.id
        existing_subscription.start_date = start_date
        existing_subscription.end_date = end_date
        db.commit()
        db.refresh(existing_subscription)
        subscription = existing_subscription
        action = "updated"
    else:
        new_subscription = UserSubscription(
            user_id=current_user.id,
            plan_id=plan.id,
            start_date=start_date,
            end_date=end_date
        )
        db.add(new_subscription)
        db.commit()
        db.refresh(new_subscription)
        subscription = new_subscription
        action = "created"

    # 4️⃣ Generate Invoice PDF
    transaction_id, invoice_path = generate_invoice(current_user, plan)

    # 5️⃣ Save Billing History
    billing = BillingHistory(
        user_id=current_user.id,
        plan_id=plan.id,
        transaction_id=transaction_id,
        invoice_path=invoice_path
    )

    db.add(billing)
    db.commit()

    return {
        "message": f"Subscription {action} successfully",
        "plan_name": plan.name,
        "price": plan.price,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date,
        "transaction_id": transaction_id,
        "invoice_file_path": invoice_path
    }


# =========================================================
# Get Current Subscription
# =========================================================
@router.get("/my-plan")
def get_my_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    subscription = db.query(UserSubscription).filter(
        UserSubscription.user_id == current_user.id
    ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")

    # Check if expired
    if subscription.end_date < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Subscription expired")

    return {
        "plan_name": subscription.plan.name,
        "price": subscription.plan.price,
        "start_date": subscription.start_date,
        "end_date": subscription.end_date
    }