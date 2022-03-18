import datetime

from fastapi import HTTPException
from sqlalchemy import and_, exists
from sqlalchemy.orm import Query, Session, joinedload

from app.db.models.action import Action
from app.db.schemas.action import ActionCreate


def create_action(
    db: Session,
    action: ActionCreate,
) -> Action:
    db_action = Action(
        # action_source_json=action.source_json,
        name=action.name,
        description=action.description,
        action_date=datetime.date(action.year, action.month, day=action.day),
        geography_id=action.geography_id,
        action_type_id=action.action_type_id,
        # Modification date is set to date of document submission
        action_mod_date=datetime.datetime.utcnow(),
        action_source_id=action.action_source_id,
    )

    db.add(db_action)
    db.commit()
    db.refresh(db_action)

    return db_action


def is_action_exists(
    db: Session,
    action: ActionCreate,
) -> bool:
    """Returns an action by its unique constraint."""

    return db.query(
        exists().where(
            and_(
                Action.name == action.name,
                Action.action_date
                == datetime.date(action.year, action.month, action.day),
                Action.geography_id == action.geography_id,
                Action.action_type_id == action.action_type_id,
                Action.action_source_id == action.action_source_id,
            )
        )
    ).scalar()


def get_actions_query(
    db: Session,
) -> Query:
    return db.query(Action).options(joinedload(Action.documents))


def get_action(
    action_id: int,
    db: Session,
) -> Query:
    action = db.query(Action).filter(Action.action_id == action_id).first()
    if not action:
        raise HTTPException(status_code=404, detail="Action not found")
    return action
