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
router.include_router(crud_router(TenderItem, "/tender-items", ["tender-items"]))
router.include_router(crud_router(RFQ, "/rfqs", ["rfqs"]))
router.include_router(crud_router(RFQItem, "/rfq-items", ["rfq-items"]))
router.include_router(crud_router(SupplierQuote, "/supplier-quotes", ["supplier-quotes"]))
router.include_router(crud_router(QuoteItem, "/quote-items", ["quote-items"]))
router.include_router(crud_router(PurchaseOrder, "/purchase-orders", ["purchase-orders"]))
router.include_router(crud_router(POItem, "/po-items", ["po-items"]))
router.include_router(crud_router(Shipment, "/shipments", ["shipments"]))
router.include_router(crud_router(GoodsReceipt, "/goods-receipts", ["goods-receipts"]))
router.include_router(crud_router(GRNItem, "/grn-items", ["grn-items"]))
router.include_router(crud_router(Delivery, "/deliveries", ["deliveries"]))
router.include_router(crud_router(DeliveryItem, "/delivery-items", ["delivery-items"]))
router.include_router(crud_router(Attachment, "/attachments", ["attachments"]))
