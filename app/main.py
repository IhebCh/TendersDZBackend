from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import inspect

from app.core.config import settings
from app.db.session import engine
from app.models.base import Base
from app.routers import auth, clients, suppliers, tenders, tender_items

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup (for dev). Use Alembic in prod.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:5174",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.CORS_ORIGINS,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(clients.router)
app.include_router(suppliers.router)
app.include_router(tenders.router)
app.include_router(tender_items.router)

@app.get("/")
def root():
    return {"message": "✅ TenderFlow API (FastAPI + SQLAlchemy + Postgres) is up!"}
