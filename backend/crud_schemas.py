from pydantic import BaseModel


class Recipe(BaseModel):
    id: int
    title: str
    image_name: str
    instructions: list[str]
    ingredients_full: list[str | None]
    ingredients: list[str | None]

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
