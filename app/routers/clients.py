from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.db.session import get_db
from app.models.entities import Client
from app.schemas.common import ClientCreate, ClientUpdate, ClientRead
from app.deps import get_current_user

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientRead])
def list_clients(db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    rows = db.execute(select(Client)).scalars().all()
    return rows

@router.post("/", response_model=ClientRead)
def create_client(payload: ClientCreate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = Client(**payload.model_dump())
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.get("/{client_id}", response_model=ClientRead)
def get_client(client_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(Client, client_id)
    if not obj:
        raise HTTPException(404, "Client not found")
    return obj

@router.put("/{client_id}", response_model=ClientRead)
def update_client(client_id: int, payload: ClientUpdate, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    obj = db.get(Client, client_id)
    if not obj:
        raise HTTPException(404, "Client not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj); db.commit(); db.refresh(obj)
    return obj

@router.delete("/{client_id}", response_model=dict)
def delete_client(client_id: int, db: Session = Depends(get_db), _: str = Depends(get_current_user)):
    ok = db.execute(delete(Client).where(Client.id == client_id)).rowcount
    if not ok:
        raise HTTPException(404, "Client not found")
    db.commit()
    return {"ok": True}
