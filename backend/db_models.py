from sqlalchemy import (
    event,
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
    BigInteger,
    DateTime,
    Float,
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import mapped_column
from pgvector.sqlalchemy import Vector
import math

from db import Base

# TODO: compute
FEATURE_LAYER_OUT_SHAPE = (7, 7, 96)


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(BigInteger, primary_key=True)
    title = Column(String, nullable=False, index=True)
    image_name = Column(String, nullable=False, index=True)
    instructions = Column(ARRAY(String), nullable=False)
    ingredients_full = Column(ARRAY(String), nullable=False)
    ingredients = Column(ARRAY(String), nullable=False)
    image_features = Column(Vector(math.prod(FEATURE_LAYER_OUT_SHAPE)), nullable=False)


class Ingredient(Base):
    # this table is there just for ingredients search suggestions
    __tablename__ = "ingredient"

    name = Column(String, primary_key=True)
