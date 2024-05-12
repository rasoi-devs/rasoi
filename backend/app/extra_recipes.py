import json, re, requests, kaggle
from bs4 import BeautifulSoup
from tqdm import tqdm
from PIL import Image
import pandas as pd

"""
extract Indian recipes from
manually entered from gform and food.com
"""

DATASET_DIR = "dataset"
EXTRA_RECIPES_JSON = "dataset/extra_recipes.json"
EXTRA_RECIPES_JSON_DEST = "dataset/extra_recipes_processed.json"
IMAGE_SRC_DIR = "dataset/gform_imgs"
IMAGE_DEST_DIR = "dataset/extra_imgs_processed"

FOOD_COM_IMG_SRC = "dataset/food_com_imgs"


def _conv_image(filename, root=IMAGE_SRC_DIR):
    # get that image, convert to RGB jpg
    im = Image.open(f"{root}/{filename}")
    rgb_im = im.convert("RGB")
    filename_wo_ext = ".".join(filename.split(".")[:-1])
    rgb_im.save(f"{IMAGE_DEST_DIR}/{filename_wo_ext}.jpg")
    return filename_wo_ext


"""
gform
"""


def _conv_to_array(inp: str, ing: bool = False):
    inp = inp or ""
    # split by next line(s)
    result = re.split(r"\n+", inp)
    # remove numbering
    result = [re.sub(r"^\d+\.", "", x).strip() for x in result]
    # clean unnecessary noise
    result = [x for x in result if len(x) > 2]
    if ing:
        # if ingredients column, lower and strip spaces
        result = [x.lower().strip() for x in result]
    return result


recipes = []
with open(EXTRA_RECIPES_JSON, "r") as f:
    recipes: list[dict] = json.load(f)

print("start preprocessing gform recipes..")
for r in tqdm(recipes):
    r["instructions"] = _conv_to_array(r["instructions"])
    r["ingredients_full"] = _conv_to_array(r["ingredients_full"])
    r["ingredients"] = _conv_to_array(r["ingredients"], True)

    # get downloadable gdrive link
    image_link = r["image_link"].split("&")[-1][3:]
    response = requests.get(f"https://drive.google.com/file/d/{image_link}/view")

    # parse html, find image filename
    # TODO: ignore / drop the recipe, if img not found
    soup = BeautifulSoup(response.text, "html.parser")
    filename = soup.find("meta", itemprop="name")["content"]

    r["image_name"] = _conv_image(filename)

    del r["image_link"]


with open(EXTRA_RECIPES_JSON_DEST, "w") as f:
    json.dump(recipes, f, indent=2)


"""
food.com
"""
print("start download and append food.com...")

kaggle.api.authenticate()
kaggle.api.dataset_download_file(
    "irkaal/foodcom-recipes-and-reviews",
    "recipes.csv",
    path=DATASET_DIR,
    quiet=False,
)

df: pd.DataFrame = pd.read_csv(
    f"{DATASET_DIR}/recipes.csv.zip",
    usecols=[
        "RecipeId",
        "RecipeCategory",
        "RecipeInstructions",
        "Name",
        "Images",
        "RecipeIngredientParts",
    ],
)
df = df.rename(
    columns={
        "RecipeId": "id",
        "RecipeCategory": "category",
        "RecipeInstructions": "instructions",
        "Name": "title",
        "Images": "images",
        "RecipeIngredientParts": "ingredients",
    },
)

df = df.dropna()
df = df.query("category == 'Indian'")


def _arr_conv(x, lower=False):
    res = [y.replace('"', "").strip() for y in x.strip("c()").split(",") if y != ""]
    if lower:
        res = [x.lower() for x in res]
    return res


def _get_first_img(x):
    splt = x.split('"')
    try:
        url = splt[1]
        img_data = requests.get(url).content
        filename = url.split("/")[-1]
        with open(f"{FOOD_COM_IMG_SRC}/{filename}", "wb") as f:
            f.write(img_data)
        return _conv_image(filename, FOOD_COM_IMG_SRC)
    except:
        return None


df["ingredients"] = df["ingredients"].apply(lambda x: _arr_conv(x, True))
df["ingredients_full"] = df["ingredients"]
df["instructions"] = df["instructions"].apply(_arr_conv)

# somehow get the image
df["image_name"] = df["images"].apply(_get_first_img)

# NOTE: this will drop null image recipes
df = df.dropna(subset=["image_name"])

df = df.drop(columns=["images", "id", "category"])

recipes.extend(df.to_dict(orient="records"))
with open(EXTRA_RECIPES_JSON_DEST, "w") as f:
    json.dump(recipes, f, indent=2)


print("done")
