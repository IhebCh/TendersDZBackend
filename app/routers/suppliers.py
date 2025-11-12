from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.session import get_db
from app.models.entities import Supplier
from app.schemas.common import SupplierCreate, SupplierUpdate, SupplierRead
from app.deps import get_current_user

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("/", response_model=list[SupplierRead])
def list_suppliers(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    return db.execute(select(Supplier)).scalars().all()

@router.post("/", response_model=SupplierRead)
def create_supplier(payload: SupplierCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = Supplier(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{supplier_id}", response_model=SupplierRead)
def get_supplier(supplier_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(Supplier, supplier_id)
    if not obj: raise HTTPException(404, "Supplier not found")
    return obj

@router.put("/{supplier_id}", response_model=SupplierRead)
def update_supplier(supplier_id: int, payload: SupplierUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(Supplier, supplier_id)
    if not obj: raise HTTPException(404, "Supplier not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{supplier_id}", response_model=dict)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    ok = db.execute(delete(Supplier).where(Supplier.id == supplier_id)).rowcount
    if not ok: raise HTTPException(404, "Supplier not found")
    db.commit()
    return {"ok": True}
