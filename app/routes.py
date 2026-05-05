from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal



router = APIRouter()

# Залежність: отримаємо сесію бази даних
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST /plans/ — створення нового плану
@router.post("/plans/", response_model=schemas.PlanOut)
def create_plan(plan: schemas.PlanCreate, db: Session = Depends(get_db)):
    db_plan = models.Plan(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

# GET /plans/{plan_date} — отримати план за датою
@router.get("/plans/{plan_date}", response_model=list[schemas.PlanOut])
def get_plans(plan_date: str, db: Session = Depends(get_db)):
    from datetime import datetime
    try:
        target_date = datetime.strptime(plan_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Неправильний формат дати. Використовуйте YYYY-MM-DD")

    plans = db.query(models.Plan).filter(models.Plan.date == target_date).all()
    return plans
