import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import Base, engine, get_db
import models
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

app = FastAPI(title="Oiltracker API", version="0.1.0")

# Create tables
Base.metadata.create_all(bind=engine)

# --- Pydantic schemas ---
class GradeIn(BaseModel):
    grade_name: str
    code_reuters: Optional[str] = None
    pricing_type: models.PricingType
    origin: Optional[str] = None

class GradeOut(GradeIn):
    grade_id: int
    class Config:
        from_attributes = True

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/grades", response_model=GradeOut)
def create_grade(grade: GradeIn, db: Session = Depends(get_db)):
    g = models.Grade(**grade.model_dump())
    db.add(g)
    db.commit()
    db.refresh(g)
    return g

@app.get("/grades", response_model=List[GradeOut])
def list_grades(db: Session = Depends(get_db)):
    return db.query(models.Grade).all()

class MarketDataIn(BaseModel):
    grade_id: int
    date: date
    price_fob_cif: float
    usd_tnd_rate: float
    source: str

class MarketDataOut(MarketDataIn):
    market_id: int
    class Config:
        from_attributes = True

@app.post("/market_data", response_model=MarketDataOut)
def add_market(m: MarketDataIn, db: Session = Depends(get_db)):
    rec = models.MarketData(**m.model_dump())
    db.add(rec)
    db.commit()
    db.refresh(rec)
    return rec

@app.get("/market_data", response_model=List[MarketDataOut])
def list_market(grade_id: Optional[int] = None, db: Session = Depends(get_db)):
    q = db.query(models.MarketData)
    if grade_id:
        q = q.filter(models.MarketData.grade_id == grade_id)
    return q.order_by(models.MarketData.date.desc()).limit(200).all()
