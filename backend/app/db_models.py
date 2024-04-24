from sqlalchemy import (
    Boolean,
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
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
import math

from .db import Base

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

    ratings = relationship("Rating", back_populates="recipe")
    comments = relationship("Comment", back_populates="recipe")


class Ingredient(Base):
    # this table is there just for ingredients search suggestions
    __tablename__ = "ingredient"

    name = Column(String, primary_key=True)


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=False, index=True, unique=True)
    hashed_password = Column(String, nullable=False)
    active = Column(Boolean, nullable=False, default=True)

    ratings = relationship("Rating", back_populates="user")
    comments = relationship("Comment", back_populates="user")


class Rating(Base):
    __tablename__ = "rating"

    id = Column(BigInteger, primary_key=True)
    # TODO: UTC time
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    rate = Column(Integer, nullable=False)

    # TODO: cascade?
    user_id = Column(ForeignKey("user.id"))
    recipe_id = Column(ForeignKey("recipe.id"))
    user = relationship("User", back_populates="ratings")
    recipe = relationship("Recipe", back_populates="ratings")



class Comment(Base):
    __tablename__ = "comment"

    id = Column(BigInteger, primary_key=True)
    # TODO: UTC time
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    content = Column(String, nullable=False)

    # TODO: cascade?
    user_id = Column(ForeignKey("user.id"))
    recipe_id = Column(ForeignKey("recipe.id"))
    user = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")
