from fastapi import FastAPI, Query
import uvicorn, spacy, json
from fastapi.middleware.cors import CORSMiddleware
from .middlewares import LimitUploadSize
from .db import engine
from fastapi.staticfiles import StaticFiles
from . import db_models
from .routers import auth, recommendations, recipes, search

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rasoi API")

IMAGES_LOC = "dataset/Food Images/Food Images"
# INGREDIENTS_JSON_LOC = f"dataset/ingredients_nlg.json"
INGREDIENTS_JSON_LOC = f"dataset/ingredients_food_com.json"

app.mount("/recipe-images", StaticFiles(directory=IMAGES_LOC), name="recipe-images")

nlp = spacy.load("en_core_web_sm")

possible_ingredients = set()
try:
    f = open(INGREDIENTS_JSON_LOC, "r")
except FileNotFoundError:
    raise Exception(
        "Ingredients dataset not found.\n"
        + "Please run `python ingredients_food_com.py` to extract all possible ingredients."
    )
else:
    with f:
        possible_ingredients.update(json.load(f)["possible_ingredients"])

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


@app.get("/short-ingredients")
def short_ingredients(q: list[str] = Query()):
    q = [x.lower().strip() for x in q if x.strip() != ""]
    result = set()
    for word in q:
        doc = nlp(word)
        for token in doc:
            # lemma of token = base word that has been converted through lemmatization
            # like: lemma(words) = word, lemma(caring) = care
            # Stemming: The word "caring" would be stemmed to "car".
            # Lemmatization: The word "caring" would be lemmatized to "care"
            ing = token.lemma_
            if ing in possible_ingredients:
                result.add(ing)
    return list(result)


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
