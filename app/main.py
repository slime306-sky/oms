from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.routes import router as auth_router
from app.core.database import Base, engine
from app.core.errors import (
    http_exception_handler,
    validation_exception_handler,
    unhandled_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Import all models so they're registered on Base.metadata before create_all runs.
from app.database.models import (  # noqa: F401
    users,
    employee,
    department,
    family_member,
    main_admin,
    refresh_token,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creates any tables that don't exist yet. Safe to run every startup —
    # it's a no-op for tables that already exist. Swap this for Alembic
    # migrations once you need schema changes on an existing database.
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


@app.get("/health")
@app.get("/")
def health():
    return {"status": "ok"}