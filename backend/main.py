from typing import Union, Annotated

from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel
import uvicorn
from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi.middleware.cors import CORSMiddleware

from db import engine, SessionLocal
import db_models, crud_schemas

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rasoi API")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    return (
        db.query(db_models.Recipe)
        .filter(db_models.Recipe.id == id)
        .order_by(db_models.Recipe.title)
        .first()
    )


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


@app.get("/recipes-from-ingredients", response_model=list[crud_schemas.Recipe])
def recipes_from_ingredients(
    q: Annotated[list[str], Query()], db: Session = Depends(get_db)
):
    q = [x.lower() for x in q]
    return (
        db.query(db_models.Recipe)
        .join(db_models.RecipeIngredient)
        .filter(db_models.RecipeIngredient.c.ingredient_name.in_(q))
        .group_by(db_models.Recipe)
        .having(func.count(db_models.RecipeIngredient.c.ingredient_name) >= len(q))
        # .order_by(db_models.Recipe.title)
        .limit(20)
        .all()
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
