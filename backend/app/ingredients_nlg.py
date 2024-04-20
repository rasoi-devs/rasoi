import pandas as pd
import kaggle
from tqdm import tqdm
import json, ast

# RecipeNLG is a gigantic dataset of recipes.
# We can use this to get a reference list of all possiible ingredients.

DATASET_DIR = "dataset"
N_LINES = 22_31_142

kaggle.api.authenticate()
kaggle.api.dataset_download_file(
    "paultimothymooney/recipenlg",
    "RecipeNLG_dataset.csv",
    path=DATASET_DIR,
    quiet=False,
)

ingredients = set()

print("extracting ingredients to memory...")
pbar = tqdm(total=N_LINES)
for chunk in pd.read_csv(f"{DATASET_DIR}/RecipeNLG_dataset.csv.zip", chunksize=50000):
    chunk: pd.DataFrame = chunk
    # lists are already in pythonic format, so just use ast
    chunk["NER"].apply(lambda x: ingredients.update(ast.literal_eval(x)))
    pbar.update(len(chunk))
pbar.close()


# cleanup
def _is_legal(word):
    word = word.strip().lower()
    return (
        (word != "")
        and len(word) > 2
        and all(ord(c) >= 97 and ord(c) <= 122 for c in word)
    )


ingredients = [i.strip().lower() for i in ingredients if _is_legal(i)]

print("writing ingredients...")
with open(f"{DATASET_DIR}/ingredients_nlg.json", "w") as f:
    json.dump(
        {"possible_ingredients": ingredients},
        f,
        separators=(",", ":"),
    )

print("done.")
