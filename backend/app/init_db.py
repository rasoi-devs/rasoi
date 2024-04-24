import pandas as pd
from .db import engine
from . import db_models
import ast, shutil, json
from glob import glob
from sqlalchemy.types import String
from sqlalchemy.dialects.postgresql import ARRAY
import spacy, math, json, kaggle
from tqdm import tqdm

from sqlalchemy.dialects.postgresql import insert
from pgvector.sqlalchemy import Vector
from sqlalchemy import text

from keras.applications import MobileNetV3Small
from keras.applications.mobilenet_v3 import preprocess_input
from keras import Model
from keras.preprocessing import image
import numpy as np

nlp = spacy.load("en_core_web_sm")

DATASET_DIR = "dataset"

EXTRA_RECIPES_JSON = "dataset/extra_recipes_processed.json"
EXTRA_IMGS_DIR = "dataset/extra_imgs_processed"

CSV_LOC = (
    f"{DATASET_DIR}/Food Ingredients and Recipe Dataset with Image Name Mapping.csv"
)
IMAGES_LOC = f"{DATASET_DIR}/Food Images/Food Images"
# INGREDIENTS_JSON_LOC = f"{DATASET_DIR}/ingredients_nlg.json"
INGREDIENTS_JSON_LOC = f"{DATASET_DIR}/ingredients_food_com.json"
N_ROWS = 13500
RECREATE = True
BATCH_SIZE = 256
# TODO: compute
FEATURE_LAYER_OUT_SHAPE = (7, 7, 96)


possible_ingredients = set()
try:
    f = open(INGREDIENTS_JSON_LOC, "r")
except FileNotFoundError:
    raise Exception(
        "Ingredients dataset not found.\n"
        + "Please run `python ingredients_nlg.py` to extract all possible ingredients."
    )
else:
    with f:
        possible_ingredients.update(json.load(f)["possible_ingredients"])


kaggle.api.authenticate()
kaggle.api.dataset_download_files(
    "pes12017000148/food-ingredients-and-recipe-dataset-with-images",
    path=DATASET_DIR,
    # unzip=True,
    quiet=False,
)


# NOTE: mobilenet is faster
base_model = MobileNetV3Small(
    weights="imagenet",
    include_top=False,
    pooling="avg",
    # optional input shape is provided, just to suppress a warning
    # by default, model accepts (224, 224, 3)
    input_shape=(224, 224, 3),
)

print("copying all extra images...")
for filepath in glob(f"{EXTRA_IMGS_DIR}/*.jpg"):
    shutil.copy(filepath, IMAGES_LOC)

# features layer should be an intermediate layer (last layer is for classification)
features_layer = base_model.get_layer("expanded_conv_10_project").output
model = Model(inputs=base_model.input, outputs=features_layer)


def _extract_features_batch(image_names, batch_size=BATCH_SIZE):
    # NOTE: to understand working of this function
    # see for a similar function (_extract_features in image_search.py file
    batch_features = []
    batch_images = []
    for image_name in image_names:
        try:
            img = image.load_img(
                f"{IMAGES_LOC}/{image_name}.jpg", target_size=(224, 224)
            )
            img_array = image.img_to_array(img)
        except:
            print(f"WARNING: {image_name}.jpg not found")
            # FIXME what if image not found?
            img_array = np.zeros((224, 224, 3))
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        batch_images.append(img_array)

    batch_images = np.vstack(batch_images)
    features = model.predict(batch_images, batch_size=batch_size, verbose=0)
    for feature in features:
        batch_features.append(feature.flatten())
    return np.array(batch_features).astype("float32")


def _extract_ingredients(sentence):
    result = set()
    for word in sentence:
        doc = nlp(word)
        for token in doc:
            # if token.pos_ == "NOUN" and not token.is_stop and token.is_alpha:

            # lemma of token = base word that has been converted through lemmatization
            # like: lemma(words) = word, lemma(caring) = care
            # Stemming: The word "caring" would be stemmed to "car".
            # Lemmatization: The word "caring" would be lemmatized to "care"
            ing = token.lemma_
            if ing in possible_ingredients:
                result.add(ing)
    return list(result)


def _sql_insert_ingredients(table, conn, keys, data_iter) -> int:
    ingredients = []
    for row in data_iter:
        ingredients.extend(row[1])
    if len(ingredients) == 0:
        return 0
    statement = (
        insert(db_models.Ingredient)
        .values([{"name": i} for i in ingredients])
        .on_conflict_do_nothing()
    )
    result = conn.execute(statement)
    return result.rowcount


if RECREATE:
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    db_models.Base.metadata.drop_all(bind=engine)
    db_models.Base.metadata.create_all(bind=engine)


"""
from extra recipes (gform + food.com)
"""
print("uploading extra recipes...")

N_EXTRAS = 0
with open(EXTRA_RECIPES_JSON, "r") as f:
    N_EXTRAS = len(json.load(f))

df = pd.read_json(EXTRA_RECIPES_JSON, orient="records")
df["image_features"] = list(
    _extract_features_batch(df["image_name"], batch_size=len(df))
)

df.to_sql(
    name="recipe",
    index=False,
    con=engine,
    if_exists="append",
    dtype={
        "ingredients_full": ARRAY(String),
        "ingredients": ARRAY(String),
        "instructions": ARRAY(String),
        "image_features": Vector(math.prod(FEATURE_LAYER_OUT_SHAPE)),
    },
)

# TODO: why do this? just insert from possible_ingredients?
df["ingredients"].to_sql(
    name="ingredient",
    con=engine,
    if_exists="append",
    method=_sql_insert_ingredients,
)


"""
from actual dataset
"""
print("uploading from main dataset...")

pbar = tqdm(total=N_ROWS)
for df in pd.read_csv(CSV_LOC, index_col=0, chunksize=BATCH_SIZE):
    df: pd.DataFrame = df.rename(
        columns={
            "Title": "title",
            "Ingredients": "ingredients_full",
            "Instructions": "instructions",
            "Image_Name": "image_name",
        }
    )

    df = df.dropna()

    df["ingredients_full"] = df["ingredients_full"].apply(lambda x: ast.literal_eval(x))
    df["instructions"] = df["instructions"].apply(
        lambda x: [y.strip() for y in str(x).split(".") if y.strip() != ""]
    )

    # Cleaned_Ingredients is useless column, create a ingredients NER column
    df = df.drop(columns=["Cleaned_Ingredients"])
    df["ingredients"] = df["ingredients_full"].apply(_extract_ingredients)

    df["image_features"] = list(_extract_features_batch(df["image_name"]))

    df.to_sql(
        name="recipe",
        index=False,
        con=engine,
        if_exists="append",
        dtype={
            "ingredients_full": ARRAY(String),
            "ingredients": ARRAY(String),
            "instructions": ARRAY(String),
            "image_features": Vector(math.prod(FEATURE_LAYER_OUT_SHAPE)),
        },
    )

    # TODO: why do this? just insert from possible_ingredients?
    df["ingredients"].to_sql(
        name="ingredient",
        con=engine,
        if_exists="append",
        method=_sql_insert_ingredients,
    )

    pbar.update(len(df))
pbar.close()

print("done.")
