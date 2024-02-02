from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .views import api

app = FastAPI()
app.include_router(api, prefix="/api/v1")
app.mount("/pub", StaticFiles(directory="pub", html=True), name="frontend")
