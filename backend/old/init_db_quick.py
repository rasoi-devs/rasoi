from sqlalchemy.engine import Connection
from sqlalchemy import Table, event, text
from sqlalchemy.orm import Session
from db import SessionLocal, engine
import db_models
import kaggle
import ast
from sqlalchemy.dialects.postgresql import insert

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


def upload_to_db():
    session = SessionLocal()

    print(f"Start writing, chunksize = {CHUNKSIZE}...")
    with pd.read_csv(
        CSV_LOC, chunksize=CHUNKSIZE, index_col=0, nrows=LINES_TO_CONSIDER
    ) as reader:
        pbar = tqdm(total=(LINES_TO_CONSIDER or N_LINES))

        for idx, chunk in enumerate(reader):
            # with session.begin():
            pbar.desc = f"Chunk {idx}/{(LINES_TO_CONSIDER or N_LINES)//CHUNKSIZE}"

            for idx, row in chunk.iterrows():

                ingredients = list(
                    set([x.lower() for x in ast.literal_eval(row["NER"]) if x != ""])
                )
                if len(ingredients) == 0:
                    continue

                try:
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

                    session.execute(
                        insert(db_models.Ingredient)
                        .values([{"name": i} for i in ingredients])
                        .on_conflict_do_nothing()
                    )
                    session.execute(
                        insert(db_models.RecipeIngredient).values(
                            [
                                {"recipe_id": recipe.id, "ingredient_name": i}
                                for i in ingredients
                            ]
                        )
                    )

                    session.commit()
                    pbar.update(1)
                except:
                    print("Problem with recipe: ", recipe.title, ingredients)
        pbar.close()
    print("done uploading...\n")


if __name__ == "__main__":
    download_dataset()
    upload_to_db()
