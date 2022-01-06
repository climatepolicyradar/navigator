import typing as t
import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from app.core.security import get_password_hash


def get_user(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_user_by_email(db: Session, email: str) -> schemas.UserBase:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> t.List[schemas.UserOut]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()
    return user


def edit_user(db: Session, user_id: int, user: schemas.UserEdit) -> schemas.User:
    db_user = get_user(db, user_id)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="User not found")
    update_data = user.dict(exclude_unset=True)

    if "password" in update_data:
        update_data["hashed_password"] = get_password_hash(user.password)
        del update_data["password"]

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_document(
    db: Session,
    document: schemas.DocumentCreate,
) -> models.Document:

    db_document = models.Document(
        action_id=document.action_id,
        name=document.name,
        language_id=document.language_id,
        source_url=document.source_url,
        s3_url=document.s3_url,
        document_date=datetime.date(document.year, document.month, document.day),
        document_mod_date=document.document_mod_date,
    )

    db.add(db_document)
    db.commit()
    db.refresh(db_document)

    return db_document


def create_action(
    db: Session,
    action: schemas.ActionCreate,
) -> models.Action:

    db_action = models.Action(
        action_source_json=action.source_json,
        name=action.name,
        description=action.description,
        action_date=datetime.date(action.year, action.month, action.day),
        geography_id=action.geography_id,
        action_type_id=action.type_id,
        action_mod_date=action.mod_date,
        action_source_id=action.source_id,
    )

    db.add(db_action)
    db.commit()
    db.refresh(db_action)

    return db_action
