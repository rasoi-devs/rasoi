from sqlalchemy import event, Column, ForeignKey, Integer, String, ARRAY, Table
from sqlalchemy.orm import relationship


from db import Base


RecipeIngredient = Table(
    "recipe_ingredient",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("recipe_id", Integer, ForeignKey("recipe.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredient.id")),
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
        # backref="Recipe",
        back_populates="recipes",
    )


class Ingredient(Base):
    __tablename__ = "ingredient"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)

    recipes = relationship(
        "Recipe",
        secondary=RecipeIngredient,
        # backref="Ingredient",
        back_populates="ingredients",
    )
