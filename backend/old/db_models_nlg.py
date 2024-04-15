from sqlalchemy import event, Column, ForeignKey, Integer, String, ARRAY, Table
from sqlalchemy.orm import relationship


from db import Base


RecipeIngredient = Table(
    "recipe_ingredient",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("recipe_id", Integer, ForeignKey("recipe.id")),
    Column("ingredient_name", String, ForeignKey("ingredient.name")),
)


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True, nullable=False)
    full_ingredients = Column(ARRAY(String), nullable=False)
    directions = Column(ARRAY(String), nullable=False)
    link = Column(String, nullable=False)
    source = Column(String, nullable=False)

    ingredients = relationship(
        "Ingredient",
        secondary=RecipeIngredient,
        back_populates="recipes",
    )


class Ingredient(Base):
    __tablename__ = "ingredient"

    # only one column, so that insertion is blazingly fast
    # (sql: insert, on conflict do nothing)
    name = Column(String, primary_key=True)

    recipes = relationship(
        "Recipe",
        secondary=RecipeIngredient,
        back_populates="ingredients",
    )
