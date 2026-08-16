from fastapi import FastAPI

from app.routers import artists

app = FastAPI()

app.include_router(artists.router)