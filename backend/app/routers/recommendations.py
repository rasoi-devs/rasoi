from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud_schemas, db_models
from ..auth import get_current_user
from ..dependencies import get_similar_by_ingredients


router = APIRouter(
    prefix="/recommendations",
    tags=["recommendations"],
    dependencies=[Depends(get_db)],
)


@router.get("/", response_model=list[crud_schemas.Recipe])
def recommendations(page: int = 0, db: Session = Depends(get_db)):
    return (
        db.query(db_models.Recipe)
        .order_by(db_models.Recipe.title)
        .offset(page * 10)
        .limit(10)
        .all()
    )


@router.get("/personalized", response_model=list[crud_schemas.Recipe])
def personalized_recommendations(
    page: int = 0,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user),
):
    # get "engagements"
    engaged_recipes = set()
    engaged_recipes.update([r.recipe for r in current_user.ratings])
    engaged_recipes.update([c.recipe for c in current_user.comments])

    # get engagements' ingredients
    all_ingredients = set()
    for r in engaged_recipes:
        all_ingredients.update(r.ingredients)

    # get similar by ingredients
    return get_similar_by_ingredients(
        ingredients=list(all_ingredients),
        db=db,
        recipe_ids_to_exclude=[r.id for r in engaged_recipes],
        skip=page * 10,
        limit=10,
    )
