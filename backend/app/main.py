from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from .middlewares import LimitUploadSize
from .db import engine
from fastapi.staticfiles import StaticFiles
from . import db_models
from .routers import auth, recommendations, recipes, search

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rasoi API")

IMAGES_LOC = "dataset/Food Images/Food Images"

app.mount("/recipe-images", StaticFiles(directory=IMAGES_LOC), name="recipe-images")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
_3_mb = 3_000_000  # 3 mb in bytes
app.add_middleware(LimitUploadSize, max_upload_size=_3_mb)

app.include_router(recommendations.router)
app.include_router(recipes.router)
app.include_router(search.router)
app.include_router(auth.router)


@app.get("/")
def index():
    return {"success": True, "message": "Docs at /docs or /redoc"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
