from fastapi import APIRouter
from app.routers.crud_base import crud_router
from app.models.entities import (
    Client, Supplier, Tender, TenderItem, RFQ, RFQItem, SupplierQuote, QuoteItem,
    PurchaseOrder, POItem, Shipment, GoodsReceipt, GRNItem, Delivery, DeliveryItem, Attachment
)

router = APIRouter()
router.include_router(crud_router(Client, "/clients", ["clients"]))
router.include_router(crud_router(Supplier, "/suppliers", ["suppliers"]))
router.include_router(crud_router(Tender, "/tenders", ["tenders"]))
router.include_router(crud_router(TenderItem, "/tender_items", ["tender_items"]))
router.include_router(crud_router(RFQ, "/rfqs", ["rfqs"]))
router.include_router(crud_router(RFQItem, "/rfq_items", ["rfq_items"]))
router.include_router(crud_router(SupplierQuote, "/supplier_quotes", ["supplier_quotes"]))
router.include_router(crud_router(QuoteItem, "/quote_items", ["quote_items"]))
router.include_router(crud_router(PurchaseOrder, "/purchase_orders", ["purchase_orders"]))
router.include_router(crud_router(POItem, "/po_items", ["po_items"]))
router.include_router(crud_router(Shipment, "/shipments", ["shipments"]))
router.include_router(crud_router(GoodsReceipt, "/goods_receipts", ["goods_receipts"]))
router.include_router(crud_router(GRNItem, "/grn_items", ["grn_items"]))
router.include_router(crud_router(Delivery, "/deliveries", ["deliveries"]))
router.include_router(crud_router(DeliveryItem, "/delivery_items", ["delivery_items"]))
router.include_router(crud_router(Attachment, "/attachments", ["attachments"]))
