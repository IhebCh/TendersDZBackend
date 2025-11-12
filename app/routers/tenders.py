from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.session import get_db
from app.models.entities import Tender
from app.schemas.common import TenderCreate, TenderUpdate, TenderRead
from app.deps import get_current_user

router = APIRouter(prefix="/tenders", tags=["Tenders"])

@router.get("/", response_model=list[TenderRead])
def list_tenders(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    return db.execute(select(Tender)).scalars().all()

@router.post("/", response_model=TenderRead)
def create_tender(payload: TenderCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = Tender(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{tender_id}", response_model=TenderRead)
def get_tender(tender_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(Tender, tender_id)
    if not obj: raise HTTPException(404, "Tender not found")
    return obj

@router.put("/{tender_id}", response_model=TenderRead)
def update_tender(tender_id: int, payload: TenderUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(Tender, tender_id)
    if not obj: raise HTTPException(404, "Tender not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{tender_id}", response_model=dict)
def delete_tender(tender_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    ok = db.execute(delete(Tender).where(Tender.id == tender_id)).rowcount
    if not ok: raise HTTPException(404, "Tender not found")
    db.commit()
    return {"ok": True}
