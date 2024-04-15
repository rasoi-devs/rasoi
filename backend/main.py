from fastapi import FastAPI, Depends, HTTPException, UploadFile, Query
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware
from middlewares import LimitUploadSize
from db import engine, SessionLocal
import db_models, crud_schemas
from image_search import extract_image_features
from fastapi.staticfiles import StaticFiles

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rasoi API")

IMAGES_LOC = "dataset/archive/Food Images/Food Images"
UPLOADS_DIR = "uploads"

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


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Recommendation(BaseModel):
    title: str
    description: str


@app.get("/")
def index():
    return {"success": True}


@app.get("/recommendations", response_model=list[Recommendation])
def recommendations():
    return [
        {
            "title": "No-Bake Nut Cookies",
            "description": "In a heavy 2-quart saucepan, mix brown sugar, nuts, evaporated milk and butter or margarine.",
        },
        {
            "title": "Jewell Ball'S Chicken",
            "description": "Place chipped beef on bottom of baking dish.",
        },
        {
            "title": "Creamy Corn",
            "description": "In a slow cooker, combine all ingredients. Cover and cook on low for 4 hours or until heated throu...",
        },
        {
            "title": "Chicken Funny",
            "description": "Boil and debone chicken.",
        },
        {
            "title": "Reeses Cups(Candy)",
            "description": "Combine first four ingredients and press in 13 x 9-inch ungreased pan.",
        },
        {
            "title": "Cheeseburger Potato Soup",
            "description": "Wash potatoes; prick several times with a fork.",
        },
    ]


@app.get("/recipes/{id}", response_model=crud_schemas.Recipe)
def recipe_detail(id: int, db: Session = Depends(get_db)):
    recipe = (
        db.query(db_models.Recipe)
        .filter(db_models.Recipe.id == id)
        .order_by(db_models.Recipe.title)
        .first()
    )
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return recipe


@app.get("/ingredients-search", response_model=list[crud_schemas.Ingredient])
def ingredients_search(q: str, db: Session = Depends(get_db)):
    # lower is slight faster than ilike
    q = q.lower()
    return (
        db.query(db_models.Ingredient)
        .filter(db_models.Ingredient.name.like(f"{q}%"))
        .order_by(db_models.Ingredient.name)
        .limit(10)
        .all()
    )


@app.get("/recipes-search", response_model=list[crud_schemas.Recipe])
def recipes_search(q: str, db: Session = Depends(get_db)):
    # lower is slight faster than ilike
    q = q.lower()
    return (
        db.query(db_models.Recipe)
        .filter(func.lower(db_models.Recipe.title).like(f"{q}%"))
        .order_by(db_models.Recipe.title)
        .limit(20)
        .all()
    )


@app.post("/recipes-from-image", response_model=list[crud_schemas.Recipe])
def recipes_from_image(image_file: UploadFile, db: Session = Depends(get_db)):
    # TODO: check feature id
    # TODO: security?
    filename = image_file.filename
    # random_hex = secrets.token_hex(8)
    # if not filename:
    #     filename = f"{random_hex}.jpg"
    # else:
    #     splitted = filename.split(".")
    #     filename = f"{splitted[0]}-{random_hex}.{''.join(splitted[1:])}"
    try:
        contents = image_file.file.read()
        with open(f"{UPLOADS_DIR}/{filename}", "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="File could not be uploaded.")
    finally:
        image_file.file.close()

    query_features = extract_image_features(f"{UPLOADS_DIR}/{filename}")
    return (
        db.query(db_models.Recipe)
        # also l2_distance and max_inner_product
        .order_by(db_models.Recipe.image_features.cosine_distance(query_features))
        .limit(5)
        .all()
    )


@app.get("/recipes-from-ingredients", response_model=list[crud_schemas.Recipe])
def recipes_from_ingredients(q: list[str] = Query(), db: Session = Depends(get_db)):
    q = [x.lower() for x in q]
    return (
        db.query(db_models.Recipe)
        .filter(db_models.Recipe.ingredients.contains(q))
        .limit(20)
        .all()
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
