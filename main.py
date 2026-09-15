"""
Listrix API — entrypoint.

Run locally with:  uvicorn main:app --reload
See README.md for full setup instructions.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from config import limiter, settings
from database import Base, engine
from routes import chat, contact, knowledge

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("listrix.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Deferred to app startup (not import time) so this module can be
    # imported safely without a live DB connection, e.g. in tests.
    # For production schema changes, prefer Alembic migrations over
    # relying on create_all.
    Base.metadata.create_all(bind=engine)
    logger.info("Listrix API started — database tables verified.")
    yield


app = FastAPI(
    title="Listrix API",
    description="Backend for Listrix, the AI assistant for Listora Digital Media.",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "X-Admin-Key"],
)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    # Never leak internals (stack traces, DB errors, API details) to the client.
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(status_code=500, content={"detail": "An unexpected error occurred. Please try again."})


app.include_router(chat.router, prefix="/api", tags=["Chat"])
app.include_router(contact.router, prefix="/api", tags=["Contact"])
app.include_router(knowledge.router, prefix="/api", tags=["Knowledge"])


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "Listrix API"}
