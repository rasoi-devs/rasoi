from db import SessionLocal, engine
import db_models
import kaggle
import ast
import multiprocessing as mp
from multiprocessing import Pool

import pandas as pd
from tqdm import tqdm

db_models.Base.metadata.drop_all(bind=engine)
db_models.Base.metadata.create_all(bind=engine)

CSV_LOC = "dataset/RecipeNLG_dataset.csv.zip"
N_LINES = 22_31_150
LINES_TO_CONSIDER: int | None = None

# NOTE: create chunks, pandas take a lot of time to load whole csv at once
CHUNKSIZE = 10000


def download_dataset():
    kaggle.api.authenticate()
    kaggle.api.dataset_download_file(
        "paultimothymooney/recipenlg",
        "RecipeNLG_dataset.csv",
        path="dataset",
        quiet=False,
    )


def _process_df(tup):
    i = tup[0]
    chunk = tup[1]
    session = SessionLocal()

    pbar = tqdm(total=len(chunk), desc=f"Chunk {i}")

    for idx, row in chunk.iterrows():
        ingredients = list(set([x.lower() for x in ast.literal_eval(row["NER"])]))

        recipe = db_models.Recipe(
            id=idx,
            title=row["title"],
            full_ingredients=ast.literal_eval(row["ingredients"]),
            directions=ast.literal_eval(row["directions"]),
            link=row["link"],
            source=row["source"],
        )
        session.add(recipe)
        session.flush()
        session.refresh(recipe)

        for i in ingredients:
            idb = session.query(db_models.Ingredient).filter_by(name=i).first()
            if idb != None:
                session.execute(
                    db_models.RecipeIngredient.insert().values(
                        recipe_id=recipe.id,
                        ingredient_id=idb.id,
                    )
                )
            else:
                idb = db_models.Ingredient(name=i)
                recipe.ingredients.append(idb)

        session.commit()
        pbar.update(1)
    pbar.close()
    return len(chunk)


if __name__ == "__main__":
    download_dataset()

    tasks = []
    print(f"Start writing, chunksize = {CHUNKSIZE}...")
    for i, chunk in enumerate(
        pd.read_csv(CSV_LOC, chunksize=CHUNKSIZE, index_col=0, nrows=LINES_TO_CONSIDER)
    ):
        tasks.append((i, chunk))

    print(f"Multiprocess...")
    with Pool(4) as p:
        p.map(_process_df, tasks)
    print("done uploading...\n")
