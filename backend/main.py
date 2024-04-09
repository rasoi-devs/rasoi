from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# from db import engine, SessionLocal
# import db_models

# db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Rasoi API")


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
