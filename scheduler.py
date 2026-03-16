from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime
import time


def check_scheduled_posts():

    while True:

        db: Session = SessionLocal()

        try:

            posts = db.query(models.Post).filter(
                models.Post.status == "scheduled",
                models.Post.scheduled_at <= datetime.utcnow()
            ).all()

            for post in posts:

                post.status = "published"
                post.published_at = datetime.utcnow()

            db.commit()

        finally:

            db.close()

        time.sleep(60)