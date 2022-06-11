import logging
import os
from datetime import datetime
import traceback

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from utils.database import SessionLocal
from routes import import_route, football_route

tags_metadata = [
    {
        "name": "Football API  Git Repo",
        "description": "Git Source code Repo reference",
        "externalDocs": {"description": "Git Url", "url": "https://github.com/orgs/SantexGroup"},
    }
]

app = FastAPI(
    title="Football API",
    description="Last Deployed on {date}  ".format(date=datetime.now().ctime()),
    version=os.environ.get("VERSION", "local"),
    openapi_tags=tags_metadata,
    docs_url="/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logging.exception(traceback.format_exc())
        return Response(traceback.format_exc(), status_code=500)


async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


app.include_router(import_route.router, tags=["Import Endpoints"])
app.include_router(football_route.router, tags=["Football Endpoints"])
app.middleware("http")(catch_exceptions_middleware)
app.middleware("http")(db_session_middleware)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000, log_level="info")
