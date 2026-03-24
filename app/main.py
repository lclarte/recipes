import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.routers import auth, recipes

os.makedirs("app/static/uploads", exist_ok=True)

app = FastAPI(title="Recipes", docs_url=None, redoc_url=None)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth.router)
app.include_router(recipes.router)
