from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.src.api import api_router
from backend.src.config import settings

app = FastAPI(
    title="Geo Board API",
    description=(
        "Welcome to Geo Board API documentation! Here you will able to discover "
        "all of the ways you can interact with the Geo Board API."
    ),
    debug=settings.DEBUG,
    docs_url="/api/v1/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(api_router)
