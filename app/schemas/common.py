from pydantic import BaseModel
from datetime import datetime

# ---- Client
class ClientCreate(BaseModel):
    name: str
    contact: str | None = None
    country: str | None = None
    notes: str | None = None

class ClientUpdate(BaseModel):
    name: str | None = None
    contact: str | None = None
    country: str | None = None
    notes: str | None = None

class ClientRead(ClientCreate):
    id: int
    model_config = {"from_attributes": True}

# ---- Supplier
class SupplierCreate(BaseModel):
    name: str
    contact: str | None = None
    country: str | None = None
    is_oem: bool = False
    verified: bool = False

class SupplierUpdate(BaseModel):
    name: str | None = None
    contact: str | None = None
    country: str | None = None
    is_oem: bool | None = None
    verified: bool | None = None

class SupplierRead(SupplierCreate):
    id: int
    model_config = {"from_attributes": True}

# ---- Tender
class TenderCreate(BaseModel):
    client_id: int
    title: str
    reference_no: str | None = None
    currency: str = "DZD"
    status: str = "IDENTIFIED"
    submission_deadline: datetime | None = None

class TenderUpdate(BaseModel):
    client_id: int | None = None
    title: str | None = None
    reference_no: str | None = None
    currency: str | None = None
    status: str | None = None
    submission_deadline: datetime | None = None

class TenderRead(TenderCreate):
    id: int
    model_config = {"from_attributes": True}

# ---- TenderItem
class TenderItemCreate(BaseModel):
    tender_id: int
    category: str
    description: str
    qty: float
    uom: str = "Unit"
    authenticity_required: bool = True

class TenderItemUpdate(BaseModel):
    tender_id: int | None = None
    category: str | None = None
    description: str | None = None
    qty: float | None = None
    uom: str | None = None
    authenticity_required: bool | None = None

class TenderItemRead(TenderItemCreate):
    id: int
    model_config = {"from_attributes": True}
