import datetime

from sqlalchemy import exists
from sqlalchemy.orm import Session, joinedload, Query

import app.db.models.action
import app.db.schemas.action


def create_action(
    db: Session,
    action: app.db.schemas.action.ActionCreate,
) -> app.db.models.action.Action:
    db_action = app.db.models.action.Action(
        # action_source_json=action.source_json,
        name=action.name,
        description=action.description,
        action_date=datetime.date(action.year, action.month, action.day),
        geography_id=action.geography_id,
        action_type_id=action.action_type_id,
        action_mod_date=datetime.datetime.utcnow(),
        action_source_id=action.action_source_id,
    )

    db.add(db_action)
    db.commit()
    db.refresh(db_action)

    return db_action


def is_action_exists(
    db: Session,
    action: app.db.schemas.action.ActionCreate,
) -> bool:
    """Returns an action by its unique constraint."""

    return db.query(
        exists().where(
            app.db.models.action.Action.name == action.name,
            app.db.models.action.Action.action_date
            == datetime.date(action.year, action.month, action.day),
            app.db.models.action.Action.geography_id == action.geography_id,
            app.db.models.action.Action.action_type_id == action.action_type_id,
            app.db.models.action.Action.action_source_id == action.action_source_id,
        )
    ).scalar()


def get_actions_query(
    db: Session,
) -> Query:
    return db.query(app.db.models.action.Action).options(
        joinedload(app.db.models.action.Action.documents)
    )
