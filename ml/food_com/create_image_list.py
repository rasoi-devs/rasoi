import random
from backend.db import SessionLocal
from backend.db_models import Recipe

DATASET_ROOT = "dataset"

print(f"start db query...")
db = SessionLocal()
recipes = db.query(Recipe.id, Recipe.images).filter(Recipe.images != []).all()

content = ""
for r in recipes:
    # NOTE: for each recipe there are multiple images. We will just select only 1 random image
    random_idx = random.randrange(len(r.images))
    img = r.images[random_idx]
    # filename = recipe_[recipe id]_[image index].jpg
    content += f"{img}\n\tout=images/recipe_{r.id}_{random_idx}.jpg\n"

with open(f"{DATASET_ROOT}/aria2c_links.txt", "w") as f:
    f.write(content)

print(f"wrote {len(recipes)} images list.")

# use: cd dataset && aria2c --auto-file-renaming=false --input-file=aria2c_links.txt -x 8
