from io import StringIO
import logging
from typing import cast

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.exc import IntegrityError

from app.api.api_v1.schemas.document import BulkImportValidatedResult
from app.api.api_v1.schemas.user import User, UserCreateAdmin
from app.core.auth import get_current_active_superuser
from app.core.aws import get_s3_client
from app.core.email import (
    send_new_account_email,
    send_password_reset_email,
)
from app.core.ratelimit import limiter
from app.core.validation.types import (
    ImportSchemaMismatchError,
    DocumentsFailedValidationError,
)
from app.core.validation.util import get_valid_metadata
from app.core.validation.cclw.law_policy.process_csv import (
    extract_documents,
    validated_input,
)
from app.db.crud.password_reset import (
    create_password_reset_token,
    invalidate_existing_password_reset_tokens,
)
from app.db.crud.user import (
    create_user,
    deactivate_user,
    edit_user,
    get_user,
    get_users,
)
from app.db.session import get_db

_LOGGER = logging.getLogger(__name__)

admin_users_router = r = APIRouter()

# TODO: revisit activation timeout
ACCOUNT_ACTIVATION_EXPIRE_MINUTES = 4 * 7 * 24 * 60  # 4 weeks


@r.get(
    "/users",
    response_model=list[User],
    response_model_exclude_none=True,
)
# TODO paginate
async def users_list(
    response: Response,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Gets all users"""
    users = get_users(db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    response.headers["Cache-Control"] = "no-cache, no-store, private"
    return users


@r.get(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True,
)
async def user_details(
    request: Request,
    response: Response,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Gets any user details"""
    user = get_user(db, user_id)
    response.headers["Cache-Control"] = "no-cache, no-store, private"
    return user


@r.post("/users", response_model=User, response_model_exclude_none=True)
async def user_create(
    request: Request,
    user: UserCreateAdmin,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Creates a new user"""
    try:
        db_user = create_user(db, user)
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Email already registered: {user.email}",
        )

    activation_token = create_password_reset_token(
        db, cast(int, db_user.id), minutes=ACCOUNT_ACTIVATION_EXPIRE_MINUTES
    )
    send_new_account_email(db_user, activation_token)

    return db_user


@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    response: Response,
    user_id: int,
    user: UserCreateAdmin,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Updates existing user"""
    updated_user = edit_user(db, user_id, user)

    # send_email(EmailType.account_changed, updated_user)

    response.headers["Cache-Control"] = "no-cache, no-store, private"
    return updated_user


@r.delete("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_delete(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """Deletes existing user"""
    return deactivate_user(db, user_id)


@r.post(
    "/password-reset/{user_id}", response_model=bool, response_model_exclude_none=True
)
@limiter.limit("6/minute")
async def request_password_reset(
    request: Request,
    user_id: int,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    """
    Deletes a password for a user, and kicks off password-reset flow.

    As this flow is initiated by admins, it always
    - cancels existing tokens
    - creates a new token
    - sends an email

    Also see the equivalent unauthenticated endpoint.
    """

    deactivated_user = deactivate_user(db, user_id)
    invalidate_existing_password_reset_tokens(db, user_id)
    reset_token = create_password_reset_token(db, user_id)
    send_password_reset_email(deactivated_user, reset_token)
    return True


@r.post(
    "/bulk-imports/cclw/law-policy",
    response_model=BulkImportValidatedResult,
    status_code=status.HTTP_202_ACCEPTED,
)
async def import_law_policy(
    request: Request,
    law_policy_csv: UploadFile,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
    s3_client=Depends(get_s3_client),
):
    """Process a Law/Policy data import"""
    _LOGGER.info("Received bulk import request for CCLW Law & Policy data")
    try:
        csv_reader = validated_input(
            StringIO(law_policy_csv.file.read().decode("utf8"))
        )
        valid_metadata = get_valid_metadata(db)

        encountered_errors = {}
        document_create_objects = []

        # TODO: Check for document existence?
        for validation_result in extract_documents(
            csv_reader=csv_reader, valid_metadata=valid_metadata
        ):
            if validation_result.errors:
                encountered_errors[validation_result.row] = validation_result.errors
            else:
                document_create_objects.append(validation_result.create_request)

        if encountered_errors:
            raise DocumentsFailedValidationError(
                message="File failed detailed validation.", details=encountered_errors
            )

        # TODO: BAK-1208 create documents in database
        # TODO: BAK-1209 write document specs to s3

        # TODO: Some way to monitor processing pipeline
        return BulkImportValidatedResult(document_count=len(document_create_objects))
    except ImportSchemaMismatchError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.details,
        ) from e
    except DocumentsFailedValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.details,
        ) from e
    except Exception as e:
        _LOGGER.exception("Unexpected error")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        ) from e
