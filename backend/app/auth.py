from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from . import crud_schemas, db_models
from .db import SessionLocal
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = "HS256"
# FIXME: eh, who cares about a project app's security?
ACCESS_TOKEN_EXPIRE_DAYS = 30


# TODO: salting?
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(email: str, db: Session) -> db_models.User | None:
    user: db_models.User = (
        db.query(db_models.User).filter(db_models.User.email == email).first()
    )
    if not user:
        return None
    return user


def create_user(email: str, password: str, db: Session) -> db_models.User | None:
    if get_user(email, db) is not None:
        return None
    hashed_password = pwd_context.hash(password)
    db_user = db_models.User(email=email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(
    email: str, password: str, db: Session
) -> bool | crud_schemas.User:
    user = get_user(email, db)
    if not user:
        return False
    if not pwd_context.verify(password, user.hashed_password):
        return False
    return user


def create_jwt_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    encoded_jwt = jwt.encode(
        {"sub": email, "exp": expire},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def get_current_user(token: str = Depends(oauth2_scheme)) -> db_models.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(email, SessionLocal())
    if user is None:
        raise credentials_exception
    return user
