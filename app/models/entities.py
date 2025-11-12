from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Float, ForeignKey, DateTime, Boolean, Text
from datetime import datetime
from app.models.base import Base

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    contact: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(100))
    notes: Mapped[str | None] = mapped_column(Text)

class Supplier(Base):
    __tablename__ = "suppliers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    contact: Mapped[str | None] = mapped_column(String(255))
    country: Mapped[str | None] = mapped_column(String(100))
    is_oem: Mapped[bool] = mapped_column(Boolean, default=False)
    verified: Mapped[bool] = mapped_column(Boolean, default=False)

class Tender(Base):
    __tablename__ = "tenders"
    id: Mapped[int] = mapped_column(primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"))
    title: Mapped[str] = mapped_column(String(255))
    reference_no: Mapped[str | None] = mapped_column(String(255))
    currency: Mapped[str] = mapped_column(String(10), default="DZD")
    status: Mapped[str] = mapped_column(String(50), default="IDENTIFIED")
    submission_deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=False))

    client: Mapped["Client"] = relationship()
    items: Mapped[list["TenderItem"]] = relationship(back_populates="tender", cascade="all, delete-orphan")

class TenderItem(Base):
    __tablename__ = "tender_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    tender_id: Mapped[int] = mapped_column(ForeignKey("tenders.id"))
    category: Mapped[str] = mapped_column(String(50))   # HW, SW, SPARE, SERVICE
    description: Mapped[str] = mapped_column(Text)
    qty: Mapped[float] = mapped_column(Float)
    uom: Mapped[str] = mapped_column(String(50), default="Unit")
    authenticity_required: Mapped[bool] = mapped_column(Boolean, default=True)

    tender: Mapped["Tender"] = relationship(back_populates="items")
