from typing import Dict, List
from sqlmodel import Session, select
from app.models.entities import TenderItem, SupplierQuote, QuoteItem, PurchaseOrder, POItem, GRNItem, DeliveryItem, Tender

def compare_quotes_by_tender(session: Session, tender_id: int) -> Dict[int, List[dict]]:
    items = session.exec(select(TenderItem).where(TenderItem.tender_id == tender_id)).all()
    out: Dict[int, List[dict]] = {}
    for it in items:
        quotes = session.exec(
            select(QuoteItem, SupplierQuote)
            .where(QuoteItem.tender_item_id == it.id)
            .where(QuoteItem.supplier_quote_id == SupplierQuote.id)
        ).all()
        out[it.id] = [
            {
                "supplier_quote_id": q.SupplierQuote.id,  # type: ignore
                "unit_price": q.QuoteItem.unit_price,     # type: ignore
                "brand": q.QuoteItem.brand,               # type: ignore
                "supplier_id": q.SupplierQuote.supplier_id # type: ignore
            } for q in quotes
        ]
        out[it.id].sort(key=lambda x: x["unit_price"] if x["unit_price"] is not None else 1e12)
    return out

def generate_po_from_awards(session: Session, tender_id: int, awards: Dict[int, int]) -> List[int]:
    supplier_map: Dict[int, List[QuoteItem]] = {}
    for ti_id, sq_id in awards.items():
        qi = session.exec(select(QuoteItem)
                          .where(QuoteItem.tender_item_id == ti_id)
                          .where(QuoteItem.supplier_quote_id == sq_id)).first()
        if not qi:
            raise ValueError(f"No quote item for tender_item:{ti_id} & supplier_quote:{sq_id}")
        sq = session.get(SupplierQuote, sq_id)
        supplier_map.setdefault(sq.supplier_id, []).append(qi)  # type: ignore

    po_ids: List[int] = []
    for supplier_id, qitems in supplier_map.items():
        po = PurchaseOrder(supplier_id=supplier_id, tender_id=tender_id, status="DRAFT", currency="USD")
        session.add(po); session.commit(); session.refresh(po)
        total = 0.0
        for qi in qitems:
            ti = session.get(TenderItem, qi.tender_item_id)
            line_total = (ti.qty or 0) * qi.unit_price
            total += line_total
            session.add(POItem(purchase_order_id=po.id, tender_item_id=ti.id, qty=ti.qty, unit_price=qi.unit_price))  # type: ignore
        po.total_amount = total
        session.add(po); session.commit()
        po_ids.append(po.id)  # type: ignore
    return po_ids

def remaining_to_deliver(session: Session, tender_id: int) -> List[dict]:
    items = session.exec(select(TenderItem).where(TenderItem.tender_id == tender_id)).all()
    result: List[dict] = []
    for it in items:
        from app.models.entities import POItem
        ordered = session.exec(select(POItem).where(POItem.tender_item_id == it.id)).all()
        ordered_qty = sum(x.qty or 0 for x in ordered)
        received = session.exec(select(GRNItem).where(GRNItem.tender_item_id == it.id)).all()
        received_qty = sum(x.qty_received or 0 for x in received)
        delivered = session.exec(select(DeliveryItem).where(DeliveryItem.tender_item_id == it.id)).all()
        delivered_qty = sum(x.qty_delivered or 0 for x in delivered)
        result.append({
            "tender_item_id": it.id,
            "description": it.description,
            "ordered_qty": ordered_qty,
            "received_qty": received_qty,
            "delivered_qty": delivered_qty,
            "remaining_to_deliver": max(0, (it.qty or 0) - delivered_qty)
        })
    return result
