from sqlalchemy import create_engine
from sqlalchemy.types import ARRAY, String, DateTime
from db import engine
import pandas as pd
import numpy as np
import db_models
from sqlalchemy.dialects.postgresql import insert


def download_dataset():
    import kaggle

    kaggle.api.authenticate()
    kaggle.api.dataset_download_file(
        "irkaal/foodcom-recipes-and-reviews",
        "recipes.parquet",
        path="dataset",
        quiet=False,
    )


def preprocess():
    df = pd.read_parquet("dataset/recipes.parquet")

    # camel case to snake case could be automated, but I am just being explicit
    df = df.rename(
        columns={
            "RecipeId": "id",
            "RecipeCategory": "category",
            "Calories": "calories",
            "FatContent": "fat",
            "SaturatedFatContent": "saturated_fat",
            "CholesterolContent": "cholesterol",
            "SodiumContent": "sodium",
            "CarbohydrateContent": "carbohydrate",
            "FiberContent": "fiber",
            "SugarContent": "sugar",
            "ProteinContent": "protein",
            "RecipeServings": "servings",
            "RecipeYield": "yield_",
            "RecipeInstructions": "instructions",
            #
            "Name": "name",
            "AuthorId": "author_id",
            "AuthorName": "author_name",
            "CookTime": "cook_time",
            "PrepTime": "prep_time",
            "TotalTime": "total_time",
            "DatePublished": "date_published",
            "Description": "description",
            "Images": "images",
            "Keywords": "keywords",
            "RecipeIngredientQuantities": "ingredient_quantities",
            "RecipeIngredientParts": "ingredients",
            "AggregatedRating": "rating",
            "ReviewCount": "review_count",
        },
    )

    # df = df.apply(lambda c: list(c) if isinstance(c[0], np.ndarray) else c)

    # df["images"] = df["images"].apply(lambda c: list(c) if c is not None else [])
    # df["keywords"] = df["keywords"].apply(lambda c: list(c) if c is not None else [])
    # df["ingredient_quantities"] = df["ingredient_quantities"].apply(lambda c: list(c) if c is not None else [])
    # df["ingredient_parts"] = df["ingredient_parts"].apply(lambda c: list(c) if c is not None else [])
    # df["instructions"] = df["instructions"].apply(lambda c: list(c) if c is not None else [])

    df["ingredient_parts"] = df["ingredient_parts"].apply(
        lambda x: [y.strip().lower() for y in x]
    )
    df = df.dropna(subset=["category", "name", "id", "total_time"])
    df["review_count"] = df["review_count"].fillna(0)

    return df


def insert_recipes(df: pd.DataFrame):
    df.to_sql(
        name="recipe",
        con=engine,
        if_exists="append",
        index=False,
        dtype={
            "images": ARRAY(String),
            "keywords": ARRAY(String),
            "ingredient_quantities": ARRAY(String),
            "ingredients": ARRAY(String),
            "instructions": ARRAY(String),
            "date_published": DateTime,
        },
    )


def _sql_insert_ingredients(table, conn, keys, data_iter) -> int:
    ingredients = []
    for row in data_iter:
        ingredients.extend(row[0])
    ingredients = list(set([i for i in ingredients if i is not None]))
    if len(ingredients) == 0:
        return 0
    statement = (
        insert(db_models.Ingredient)
        .values([{"name": i} for i in ingredients])
        .on_conflict_do_nothing()
    )
    result = conn.execute(statement)
    return result.rowcount


def insert_ingredients(df: pd.DataFrame):
    df["ingredient_parts"].to_sql(
        name="ingredient",
        con=engine,
        if_exists="append",
        index=False,
        method=_sql_insert_ingredients,
    )


if __name__ == "__main__":
    download_dataset()

    db_models.Base.metadata.drop_all(bind=engine)
    db_models.Base.metadata.create_all(bind=engine)

    print("preprocess...")
    df: pd.DataFrame = preprocess()

    print("inserting recipes...")
    insert_recipes(df)

    print("inserting ingredients...")
    insert_ingredients(df)

    print("done...")
