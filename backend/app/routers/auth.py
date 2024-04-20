from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..db import get_db
from .. import crud_schemas, db_models
from ..auth import (
    authenticate_user,
    create_jwt_access_token,
    create_user,
    get_current_user,
    get_user,
)
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    dependencies=[Depends(get_db)],
    responses={401: {"detail": "Could not validate credentials"}},
)


@router.post(
    "/register",
    responses={
        400: {"detail": "email and password cannot be blank."},
        409: {"detail": "Account already exists."},
        500: {"detail": "Account cannot be created."},
    },
)
def register(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> crud_schemas.Token:
    # OAuth2 uses username, but internally in this app we will be using email
    # so, email = username internally
    email = form_data.username.strip()
    password = form_data.password.strip()
    if (not email) or (not password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email and password cannot be blank.",
        )
    user = get_user(email=email, db=db)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists.",
        )
    db_user = create_user(email, password, db)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Account cannot be created.",
        )
    access_token = create_jwt_access_token(email)
    return crud_schemas.Token(
        user=db_user, access_token=access_token, token_type="bearer"
    )


@router.post("/token", responses={401: {"detail": "Incorrect username or password."}})
def token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
) -> crud_schemas.Token:
    # OAuth2 uses username, but internally in this app we will be using email
    # so, email = username internally
    user = authenticate_user(
        email=form_data.username,
        password=form_data.password,
        db=db,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_jwt_access_token(user.email)
    return crud_schemas.Token(user=user, access_token=access_token, token_type="bearer")


@router.get("/user-exists")
def user_exists(q: str = Query(), db: Session = Depends(get_db)) -> bool:
    return db.query(db_models.User).filter(db_models.User.email == q).first() != None


@router.get("/me", response_model=crud_schemas.User)
def read_users_me(current_user: db_models.User = Depends(get_current_user)):
    return current_user
