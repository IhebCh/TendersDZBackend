from typing import Type
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import SQLModel, Session, select
from app.deps import get_db, get_current_user
from app.models.user import User

def crud_router(model: Type[SQLModel], prefix: str, tags: list[str]):
    router = APIRouter(prefix=prefix, tags=tags)

    @router.get("/", response_model=list[model])  # type: ignore
    def list_items(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        return db.exec(select(model)).all()

    @router.get("/{item_id}", response_model=model)  # type: ignore
    def get_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        obj = db.get(model, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        return obj

    @router.post("/", response_model=model)  # type: ignore
    def create_item(payload: model, db: Session = Depends(get_db), user: User = Depends(get_current_user)):  # type: ignore
        db.add(payload)
        db.commit()
        db.refresh(payload)
        return payload

    @router.put("/{item_id}", response_model=model)  # type: ignore
    def update_item(item_id: int, payload: model, db: Session = Depends(get_db), user: User = Depends(get_current_user)):  # type: ignore
        obj = db.get(model, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        data = payload.model_dump(exclude_unset=True)
        for k, v in data.items():
            setattr(obj, k, v)
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @router.delete("/{item_id}", response_model=dict)
    def delete_item(item_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
        obj = db.get(model, item_id)
        if not obj:
            raise HTTPException(status_code=404, detail="Not found")
        db.delete(obj)
        db.commit()
        return {"ok": True}

    return router
