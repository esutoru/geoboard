from fastapi import FastAPI

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


# TODO: Add CORS middleware


app.include_router(api_router)
