from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from .. import crud_schemas, db_models
from ..image_search import extract_image_features
from ..dependencies import UPLOADS_DIR


router = APIRouter(
    prefix="/search",
    tags=["search"],
    dependencies=[Depends(get_db)],
)


@router.get("/ingredients", response_model=list[crud_schemas.Ingredient])
def ingredients_search(q: str = Query(), db: Session = Depends(get_db)):
    # lower is slight faster than ilike
    q = q.lower()
    return (
        db.query(db_models.Ingredient)
        .filter(db_models.Ingredient.name.like(f"{q}%"))
        .order_by(db_models.Ingredient.name)
        .limit(10)
        .all()
    )


@router.get("/recipes", response_model=list[crud_schemas.Recipe])
def recipes_search(q: str = Query(), db: Session = Depends(get_db)):
    # lower is slight faster than ilike
    q = q.lower()
    return (
        db.query(db_models.Recipe)
        .filter(func.lower(db_models.Recipe.title).like(f"{q}%"))
        .order_by(db_models.Recipe.title)
        .limit(20)
        .all()
    )


@router.get("/recipes-from-ingredients", response_model=list[crud_schemas.Recipe])
def recipes_from_ingredients(q: list[str] = Query(), db: Session = Depends(get_db)):
    q = [x.lower() for x in q]
    return (
        db.query(db_models.Recipe)
        .filter(db_models.Recipe.ingredients.contains(q))
        .limit(20)
        .all()
    )


@router.post(
    "/recipes-from-image",
    response_model=list[crud_schemas.Recipe],
    responses={500: {"detail": "File could not be uploaded."}},
)
def recipes_from_image(image_file: UploadFile, db: Session = Depends(get_db)):
    # TODO: check feature id
    # TODO: security?
    filename = image_file.filename
    # random_hex = secrets.token_hex(8)
    # if not filename:
    #     filename = f"{random_hex}.jpg"
    # else:
    #     splitted = filename.split(".")
    #     filename = f"{splitted[0]}-{random_hex}.{''.join(splitted[1:])}"
    try:
        contents = image_file.file.read()
        with open(f"{UPLOADS_DIR}/{filename}", "wb") as f:
            f.write(contents)
    except Exception:
        raise HTTPException(status_code=500, detail="File could not be uploaded.")
    finally:
        image_file.file.close()

    query_features = extract_image_features(f"{UPLOADS_DIR}/{filename}")
    return (
        db.query(db_models.Recipe)
        # also l2_distance and max_inner_product
        .order_by(db_models.Recipe.image_features.cosine_distance(query_features))
        .limit(5)
        .all()
    )
