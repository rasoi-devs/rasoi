from . import db_models
from sqlalchemy.sql import text
from sqlalchemy.orm import Session

UPLOADS_DIR = "uploads"


def get_similar_by_ingredients(
    ingredients: list[str],
    db: Session,
    recipe_ids_to_exclude: list[int],
    skip: int = 0,
    limit: int = 5,
) -> db_models.Recipe:
    igs = [x.lower() for x in ingredients]
    similar_recipes = (
        db.query(db_models.Recipe)
        .from_statement(
            text(
                """
                    SELECT *,
                    (
                        SELECT COUNT(*)
                        FROM unnest(ingredients) i
                        -- TODO: NOT IN not working
                        -- WHERE i = ANY(:igs) AND id NOT IN :rids
                        WHERE i = ANY(:igs) AND id != ALL(:rids)
                    ) AS similarity_score
                    FROM recipe
                    ORDER BY similarity_score DESC
                    LIMIT :limit
                    OFFSET :skip;
                """
            )
        )
        .params(igs=igs, rids=recipe_ids_to_exclude, skip=skip,limit=limit)
        .all()
    )
    return similar_recipes
