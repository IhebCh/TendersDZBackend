from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.deps import get_db, get_current_user
from app.models.user import User
from app.services.business import compare_quotes_by_tender, generate_po_from_awards, remaining_to_deliver

router = APIRouter(prefix="/business", tags=["business"])

@router.get("/quotes/compare/{tender_id}", response_model=dict)
def quotes_compare(tender_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return compare_quotes_by_tender(db, tender_id)

@router.post("/po/generate/{tender_id}", response_model=dict)
def po_generate(tender_id: int, awards: dict[int, int], db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    try:
        po_ids = generate_po_from_awards(db, tender_id, awards)
        return {"po_ids": po_ids}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/deliveries/remaining/{tender_id}", response_model=list[dict])
def remaining(tender_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return remaining_to_deliver(db, tender_id)
