from sqlalchemy.types import ARRAY, String
from db import engine
import backend.db_models as db_models
import ast
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import Connection, text

import pandas as pd
from tqdm import tqdm
import traceback


############################################################
############################################################
# region settings / constants
############################################################
############################################################
CSV_LOC = "dataset/RecipeNLG_dataset.csv.zip"
N_LINES = 22_31_150
LINES_TO_CONSIDER: int | None = None

# create chunks, pandas take a lot of time to load whole csv at once
# NOTE: don't increase chunksize too much or else, postgres will hit a max no of params limit (hard to debug)
CHUNKSIZE = 2000

# set this to retry on error,
# it will retry after skipping some chunks
START_CHUNK = 0


############################################################
############################################################
# region chunk / df processors
############################################################
############################################################
def _process_recipes_chunk(chunk: pd.DataFrame, conn: Connection):
    chunk.drop(columns=["NER"], inplace=True)
    chunk.rename(columns={"ingredients": "full_ingredients"}, inplace=True)

    chunk.to_sql(
        name="recipe",
        con=conn,
        if_exists="append",
        index_label="id",
        dtype={
            "full_ingredients": ARRAY(String),
            "directions": ARRAY(String),
        },
    )


def _process_ingredients_chunk(chunk: pd.DataFrame, conn: Connection):
    chunk.drop(
        columns=["title", "ingredients", "directions", "link", "source"],
        inplace=True,
    )
    chunk.rename(
        columns={"NER": "name"},
        inplace=True,
    )

    chunk.to_sql(
        name="ingredient",
        con=conn,
        if_exists="append",
        index=False,
        method=_insert_ingredients,
    )


def _process_linking(chunk: pd.DataFrame, conn: Connection):
    chunk.drop(
        columns=["title", "ingredients", "directions", "link", "source"],
        inplace=True,
    )
    chunk.rename(
        columns={"NER": "ingredients"},
        inplace=True,
    )

    chunk.to_sql(
        name="recipe_ingredient",
        con=conn,
        if_exists="append",
        method=_link_recipe_ingredient,
    )


############################################################
############################################################
# region db insert functions
############################################################
############################################################
def _insert_ingredients(table, conn, keys, data_iter):
    ingredients = []
    for row in data_iter:
        ingredients.extend(row[0])
    ingredients = list(set(ingredients))
    if len(ingredients) == 0:
        return 0
    statement = (
        insert(db_models.Ingredient)
        .values([{"name": i} for i in ingredients])
        .on_conflict_do_nothing()
    )
    result = conn.execute(statement)
    return result.rowcount


def _link_recipe_ingredient(table, conn, keys, data_iter):
    data = []
    for row in data_iter:
        data.extend(
            [{"recipe_id": row[0], "ingredient_name": i} for i in list(set(row[1]))]
        )
    if len(data) == 0:
        return 0
    statement = insert(db_models.RecipeIngredient).values(data).on_conflict_do_nothing()
    result = conn.execute(statement)
    return result.rowcount


############################################################
############################################################
# region meat
############################################################
############################################################
def download_dataset():
    import kaggle

    kaggle.api.authenticate()
    kaggle.api.dataset_download_file(
        "paultimothymooney/recipenlg",
        "RecipeNLG_dataset.csv",
        path="dataset",
        quiet=False,
    )


def _arr_conv(r: str):
    # convert CSV arrays to python arrays and clean junk characters
    return list(
        set(
            [
                x.lower()
                # CSV already contains the arrays in pythonic form, so use ast
                for x in ast.literal_eval(r)
                # 32 to 126 are printable ASCII chars
                if (x != "") and all(ord(c) >= 32 and ord(c) <= 126 for c in x)
            ]
        )
    )


def upload_to_db():
    print(f"Start uploading, chunksize = {CHUNKSIZE}...")

    with pd.read_csv(
        CSV_LOC, chunksize=CHUNKSIZE, index_col=0, nrows=LINES_TO_CONSIDER
    ) as reader:
        pbar = tqdm(total=(LINES_TO_CONSIDER or N_LINES))

        # NOTE: don't naively do itterrows (read rows line-by-line), it is excessively slow,
        # try to apply to the whole chunk/dataframe at once

        for idx, chunk in enumerate(reader):
            if (idx + 1) < START_CHUNK:
                continue

            pbar.desc = f"Chunk {idx+1}/{(LINES_TO_CONSIDER or N_LINES)//CHUNKSIZE}"

            chunk: pd.DataFrame = chunk

            # drop rows which has any column as empty
            chunk = chunk.dropna()

            # convert CSV arrays to python arrays
            chunk.loc[:, "NER"] = chunk["NER"].apply(_arr_conv)
            chunk.loc[:, "directions"] = chunk["directions"].apply(_arr_conv)
            chunk.loc[:, "ingredients"] = chunk["ingredients"].apply(_arr_conv)

            try:
                with engine.begin() as conn:
                    # insert all recipes
                    chunk_recipes: pd.DataFrame = chunk.copy()
                    _process_recipes_chunk(chunk_recipes, conn)

                    # now, insert all ingredients
                    chunk_ingredients: pd.DataFrame = chunk.copy()
                    _process_ingredients_chunk(chunk_ingredients, conn)

                    # link them
                    chunk_recipe_ingredient: pd.DataFrame = chunk.copy()
                    _process_linking(chunk_recipe_ingredient, conn)
            except Exception:
                print(traceback.format_exc())
                print("\n\n")
                print(f"Set START_CHUNK = {idx+1}")
                break

            pbar.update(len(chunk))

        pbar.close()
    print("Done uploading...\n")


if __name__ == "__main__":
    # python init_db_blazing.py > logs.txt 2>&1
    # win: python .\init_db_blazing.py 2>&1 > .\logs.txt

    if START_CHUNK == 0:
        # drop then create all the tables
        db_models.Base.metadata.drop_all(bind=engine)
        db_models.Base.metadata.create_all(bind=engine)

    download_dataset()
    upload_to_db()

    print()

    # TODO: ignore below processes for now, takes too much time

    # print("Removing all recipes having no ingredients linked...")
    # print("(ctrl+c to stop if it takes too much time)")
    # with engine.begin() as conn:
    #     result = conn.execute(
    #         text(
    #             "delete from recipe r where not exists (select * from recipe_ingredient ri where r.id = ri.recipe_id);"
    #         )
    #     )
    #     print(f"{result.rowcount} recipe(s) deleted.")

    # TODO: add PK to 'ingredient' table, unique name column
    print("TODO: add PK to 'ingredient' table, unique name column")
