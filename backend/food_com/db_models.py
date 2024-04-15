from sqlalchemy import (
    event,
    Column,
    ForeignKey,
    Integer,
    String,
    ARRAY,
    Table,
    BigInteger,
    DateTime,
    Float,
)

from db import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False)

    calories = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    saturated_fat = Column(Float, nullable=True)
    cholesterol = Column(Float, nullable=True)
    sodium = Column(Float, nullable=True)
    carbohydrate = Column(Float, nullable=True)
    fiber = Column(Float, nullable=True)
    sugar = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    rating = Column(Float, nullable=True)
    servings = Column(Integer, nullable=True)
    yield_ = Column(String, nullable=True)
    cook_time = Column(String, nullable=True)
    prep_time = Column(String, nullable=True)
    description = Column(String, nullable=True)
    images = Column(ARRAY(String), nullable=True)

    review_count = Column(Integer, nullable=False)
    author_id = Column(BigInteger, nullable=False)
    author_name = Column(String, nullable=False)
    total_time = Column(String, nullable=False)
    date_published = Column(DateTime, nullable=False)

    keywords = Column(ARRAY(String), nullable=False)
    ingredient_quantities = Column(ARRAY(String), nullable=False)
    ingredients = Column(ARRAY(String), nullable=False)
    instructions = Column(ARRAY(String), nullable=False)


class Ingredient(Base):
    # this table is there just for ingredients search suggestions
    __tablename__ = "ingredient"

    name = Column(String, primary_key=True)
