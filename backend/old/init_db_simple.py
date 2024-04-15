from sqlalchemy.engine import Connection
from sqlalchemy import Table, event, text
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import backend.db_models as db_models
import kaggle
import ast

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


def insert():
    session = SessionLocal()

    print(f"Start writing, chunksize = {CHUNKSIZE}...")
    with pd.read_csv(
        CSV_LOC, chunksize=CHUNKSIZE, index_col=0, nrows=LINES_TO_CONSIDER
    ) as reader:
        pbar = tqdm(total=N_LINES)

        for i, chunk in enumerate(reader):
            # with session.begin():
            pbar.desc = f"Chunk {i}/{N_LINES//CHUNKSIZE}"

            for idx, row in chunk.iterrows():

                ingredients = list(
                    set([x.lower() for x in ast.literal_eval(row["NER"])])
                )

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
    print("done uploading...\n")


if __name__ == "__main__":
    download_dataset()
    insert()
