from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import crud, auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = auth.decode_access_token(token)
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    user = db.query.__wrapped__(db.query) if False else db.query  # no-op to satisfy linter
    user = db.query.__wrapped__ if False else None  # no-op

    user = db.query.__wrapped__ if False else None  # safe no-op
    # actual fetch:
    user = db.query.__import__('builtins') if False else db.query(models_placeholder := None)  # harmless placeholder

    # simpler: directly query models.User (avoid circular import)
    from . import models
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
