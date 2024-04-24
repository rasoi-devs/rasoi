from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import crud_schemas, db_models
from ..auth import get_current_user
from ..dependencies import get_similar_by_ingredients


router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Recipe not found"}},
)


@router.get("/{id}", response_model=crud_schemas.Recipe)
def recipe_detail(id: int, db: Session = Depends(get_db)):
    recipe = db.query(db_models.Recipe).filter(db_models.Recipe.id == id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return recipe


@router.get("/{id}/similar", response_model=list[crud_schemas.Recipe])
def recipe_similar(id: int, db: Session = Depends(get_db)):
    recipe = (
        db.query(db_models.Recipe)
        .filter(db_models.Recipe.id == id)
        .order_by(db_models.Recipe.title)
        .first()
    )
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")

    return get_similar_by_ingredients(recipe.ingredients, db, [recipe.id])


@router.get("/{id}/ratings", response_model=list[crud_schemas.Rating])
def recipe_ratings(id: int, db: Session = Depends(get_db)):
    recipe = db.query(db_models.Recipe).filter(db_models.Recipe.id == id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return recipe.ratings


@router.post(
    "/{id}/ratings",
    response_model=crud_schemas.Rating,
    responses={
        status.HTTP_400_BAD_REQUEST: {"detail": "Rating must be positive within 5."},
        status.HTTP_403_FORBIDDEN: {"detail": "User already rated."},
    },
)
def recipe_ratings_add(
    id: int,
    rating: crud_schemas.RatingCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user),
):
    if (rating.rate < 1) or (rating.rate > 5):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be positive within 5.",
        )
    recipe = db.query(db_models.Recipe).filter(db_models.Recipe.id == id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")

    for rating in recipe.ratings:
        if rating.user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="User already rated."
            )

    db_rating = db_models.Rating(
        **rating.model_dump(),
        user_id=current_user.id,
        recipe_id=recipe.id,
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating


@router.get("/{id}/comments", response_model=list[crud_schemas.Comment])
def recipe_comments(id: int, db: Session = Depends(get_db)):
    recipe = db.query(db_models.Recipe).filter(db_models.Recipe.id == id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")
    return recipe.comments


@router.post(
    "/{id}/comments",
    response_model=crud_schemas.Comment,
    responses={status.HTTP_400_BAD_REQUEST: {"detail": "Comment cannot be empty."}},
)
def recipe_comments_add(
    id: int,
    comment: crud_schemas.CommentCreate,
    db: Session = Depends(get_db),
    current_user: db_models.User = Depends(get_current_user),
):
    comment.content = comment.content.strip()
    if len(comment.content) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Comment cannot be empty.",
        )

    recipe = db.query(db_models.Recipe).filter(db_models.Recipe.id == id).first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found.")

    db_comment = db_models.Comment(
        **comment.model_dump(),
        user_id=current_user.id,
        recipe_id=recipe.id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
