from sqlalchemy.orm import Session
from app import models

def save_plan(db: Session, date: str, content: str):
    plan = models.Plan(date=date, content=content)
    db.add(plan)
    db.commit()
    db.refresh(plan)

def get_plans_by_date(db: Session, date: str):
    return [plan.content for plan in db.query(models.Plan).filter(models.Plan.date == date).all()]
