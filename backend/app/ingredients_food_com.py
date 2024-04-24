import pandas as pd
import kaggle
from tqdm import tqdm
import json, ast

# RecipeNLG is a gigantic dataset of recipes.
# We can use this to get a reference list of all possiible ingredients.

DATASET_DIR = "dataset"
N_LINES = 5_225_17

kaggle.api.authenticate()
kaggle.api.dataset_download_file(
    "irkaal/foodcom-recipes-and-reviews",
    "recipes.csv",
    path=DATASET_DIR,
    quiet=False,
)

ingredients = set()


def _arr_conv(x, lower=False):
    res = [y.replace('"', "").strip() for y in x.strip("c()").split(",") if y != ""]
    if lower:
        res = [x.lower() for x in res]
    return res


print("extracting ingredients to memory...")
pbar = tqdm(total=N_LINES)
for chunk in pd.read_csv(f"{DATASET_DIR}/recipes.csv.zip", chunksize=50000):
    chunk: pd.DataFrame = chunk
    chunk["RecipeIngredientParts"].apply(
        lambda x: ingredients.update(_arr_conv(x, True))
    )
    pbar.update(len(chunk))
pbar.close()


# cleanup
def _is_legal(word):
    word = word.strip().lower()
    return len(word) > 2 and all(ord(c) >= 97 and ord(c) <= 122 for c in word)


ingredients = [i.strip().lower() for i in ingredients if _is_legal(i)]

print("writing ingredients...")
with open(f"{DATASET_DIR}/ingredients_food_com.json", "w") as f:
    json.dump({"possible_ingredients": ingredients}, f)

print("done.")
