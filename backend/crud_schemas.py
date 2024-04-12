from pydantic import BaseModel


class Ingredient(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Recipe(BaseModel):
    id: int
    title: str
    full_ingredients: list[str]
    directions: list[str]
    link: str
    source: str

    class Config:
        from_attributes = True


class RecipeWithIngredients(Recipe):
    ingredients: list[Ingredient]


class IngredientWithRecipes(Ingredient):
    recipes: list[Recipe]
