import logging
from io import StringIO
from typing import cast

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    HTTPException,
    Request,
    Response,
    UploadFile,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy import update

from app.api.api_v1.schemas.document import (
    BulkImportValidatedResult,
    DocumentCreateRequest,
    DocumentParserInput,
    DocumentUpdateRequest,
)
from app.api.api_v1.schemas.user import User, UserCreateAdmin
from app.core.auth import get_current_active_superuser
from app.core.aws import get_s3_client
from app.core.email import (
    send_new_account_email,
    send_password_reset_email,
)
from app.core.ratelimit import limiter
from app.core.validation import IMPORT_ID_MATCHER
from app.core.validation.types import (
    ImportSchemaMismatchError,
    DocumentsFailedValidationError,
)
from app.core.validation.util import get_valid_metadata, write_documents_to_s3
from app.core.validation.cclw.law_policy.process_csv import (
    extract_documents,
    validated_input,
)
from app.db.crud.document import create_document, write_metadata
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
from app.db.models.document import Document
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
    background_tasks: BackgroundTasks,
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
        existing_import_ids = db.query(Document.import_id).all()

        encountered_errors = {}
        document_create_objects: list[DocumentCreateRequest] = []

        import_ids_to_create = []
        # TODO: Check for document existence?
        for validation_result in extract_documents(
            csv_reader=csv_reader, valid_metadata=valid_metadata
        ):
            if validation_result.errors:
                encountered_errors[validation_result.row] = validation_result.errors
            else:
                import_ids_to_create.append(validation_result.import_id)
                document_create_objects.append(validation_result.create_request)

        if encountered_errors:
            raise DocumentsFailedValidationError(
                message="File failed detailed validation.", details=encountered_errors
            )

        documents_ids_already_exist = set(import_ids_to_create).intersection(
            set(existing_import_ids)
        )

        background_tasks.add_task(start_import, db, s3_client, document_create_objects)

        # TODO: Add some way to monitor processing pipeline...
        total_document_count = len(document_create_objects)
        document_skipped_count = len(documents_ids_already_exist)
        return BulkImportValidatedResult(
            document_count=total_document_count,
            document_added_count=total_document_count - document_skipped_count,
            document_skipped_count=document_skipped_count,
            document_skipped_ids=documents_ids_already_exist,
        )
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


def start_import(db, s3_client, document_create_objects):
    document_parser_inputs: list[DocumentParserInput] = []
    documents_ids_already_exist: list[str] = []
    try:
        # Create a savepoint & start a transaction if necessary
        with db.begin_nested():
            for dco in document_create_objects:
                existing_document = (
                    db.query(Document)
                    .filter(Document.import_id == dco.import_id)
                    .scalar()
                )
                if existing_document is None:
                    new_document = create_document(db, dco)
                    write_metadata(db, new_document, dco)

                    document_parser_inputs.append(
                        DocumentParserInput(
                            slug=cast(str, new_document.slug),
                            **dco.dict(),
                        )
                    )
                else:
                    documents_ids_already_exist.append(dco.import_id)

            # This commit is necessary after completing the nested transaction
        db.commit()
    except Exception as e:
        _LOGGER.exception("Unexpected error creating document entries")
        if isinstance(e, IntegrityError):
            raise HTTPException(409, detail="Document already exists")
        raise e

    write_documents_to_s3(s3_client=s3_client, documents=document_parser_inputs)
    return documents_ids_already_exist


@r.put("/documents/{import_id_or_slug}", status_code=status.HTTP_200_OK)
async def update_document(
    request: Request,
    import_id_or_slug: str,
    meta_data: DocumentUpdateRequest,
    db=Depends(get_db),
    current_user=Depends(get_current_active_superuser),
):
    # TODO: As this grows move it out into the crud later.

    # Note this code relies on the fields being the same as the db column names
    doc_update = update(Document)
    doc_update = doc_update.values(meta_data.dict())

    import_id = None
    slug = None

    doc_query = db.query(Document)
    if IMPORT_ID_MATCHER.match(import_id_or_slug) is not None:
        import_id = import_id_or_slug
        doc_update = doc_update.where(Document.import_id == import_id)
        doc_query = doc_query.filter(Document.import_id == import_id)
    else:
        slug = import_id_or_slug
        doc_update = doc_update.where(Document.slug == slug)
        doc_query = doc_query.filter(Document.slug == slug)

    existing_doc = doc_query.first()

    if existing_doc is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    # TODO: Enforce uniqueness on import_id and slug on "Document"
    num_changed = db.execute(doc_update).rowcount

    if num_changed == 0:
        return existing_doc  # Nothing to do - as should be idempotent

    if num_changed > 1:
        # This should never happen due to table uniqueness constraints
        # TODO Rollback
        raise HTTPException(
            detail=f"There was more than one document identified by {import_id_or_slug}. This should not happen!!!",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    db.commit()
    db.refresh(existing_doc)
    return existing_doc
