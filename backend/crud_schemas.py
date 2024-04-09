from pydantic import BaseModel


class Ingredient(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class Recipe(BaseModel):
    id: int
    title: str
    full_ingredients: list[str]
    directions: list[str]
    link: str
    source: str
    ingredients: list[Ingredient]

    class Config:
        orm_mode = True
