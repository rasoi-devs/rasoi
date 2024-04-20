from pydantic import BaseModel
from datetime import datetime


class Recipe(BaseModel):
    id: int
    name: str
    category: str

    calories: float | None
    fat: float | None
    saturated_fat: float | None
    cholesterol: float | None
    sodium: float | None
    carbohydrate: float | None
    fiber: float | None
    sugar: float | None
    protein: float | None
    rating: float | None
    servings: int | None
    yield_: str | None
    cook_time: str | None
    prep_time: str | None
    description: str | None
    images: list[str] | None

    review_count: int
    author_id: int
    author_name: str
    total_time: str
    date_published: datetime
    keywords: list[str|None]
    ingredient_quantities: list[str | None]
    ingredients: list[str|None]
    instructions: list[str]

    class Config:
        from_attributes = True


class Ingredient(BaseModel):
    name: str

    class Config:
        from_attributes = True


# class RecipeWithIngredients(Recipe):
#     ingredients: list[Ingredient]


# class IngredientWithRecipes(Ingredient):
#     recipes: list[Recipe]
