from pydantic import BaseModel
from datetime import datetime


class Recipe(BaseModel):
    id: int
    title: str
    image_name: str
    instructions: list[str]
    ingredients_full: list[str | None]
    ingredients: list[str | None]

    class Config:
        from_attributes = True


class RecipeWithSimilarRecipes(Recipe):
    similar_recipes: list[Recipe]


class Ingredient(BaseModel):
    name: str

    class Config:
        from_attributes = True


# jwt and auth stuff
class TokenData(BaseModel):
    email: str


class BaseUser(BaseModel):
    email: str


class UserCreate(BaseUser):
    password: str


class User(BaseUser):
    id: int
    active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: User

    class Config:
        from_attributes = True


class RatingCreate(BaseModel):
    rate: int


class Rating(RatingCreate):
    id: int
    created_at: datetime
    updated_at: datetime | None
    user: User
    recipe_id: int

    class Config:
        from_attributes = True
