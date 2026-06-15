# app/main.py

from fastapi import FastAPI
from app.api.auth import router

from app.api.document import router as document_router
from app.api.chat import router as chat_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://main.d3uvcsqrnjo5uf.amplifyapp.com"
    ],
    allow_origin_regex="https://.*\\.amplifyapp\\.com",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(
    router,
    prefix="/auth",
    tags=["auth"]
)

app.include_router(
    document_router,
    prefix="/documents",
    tags=["documents"]
)
app.include_router(
    chat_router,
    prefix="/chat",
    tags=["chat"]
)