from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.session import get_db
from app.models.entities import TenderItem
from app.schemas.common import TenderItemCreate, TenderItemUpdate, TenderItemRead
from app.deps import get_current_user

router = APIRouter(prefix="/tender_items", tags=["Tender Items"])

@router.get("/", response_model=list[TenderItemRead])
def list_items(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    return db.execute(select(TenderItem)).scalars().all()

@router.post("/", response_model=TenderItemRead)
def create_item(payload: TenderItemCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = TenderItem(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{item_id}", response_model=TenderItemRead)
def get_item(item_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(TenderItem, item_id)
    if not obj: raise HTTPException(404, "Tender item not found")
    return obj

@router.put("/{item_id}", response_model=TenderItemRead)
def update_item(item_id: int, payload: TenderItemUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(TenderItem, item_id)
    if not obj: raise HTTPException(404, "Tender item not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{item_id}", response_model=dict)
def delete_item(item_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    ok = db.execute(delete(TenderItem).where(TenderItem.id == item_id)).rowcount
    if not ok: raise HTTPException(404, "Tender item not found")
    db.commit()
    return {"ok": True}
