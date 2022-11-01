"""Base definitions for data ingest"""
from abc import abstractmethod, ABC
from dataclasses import dataclass
from typing import Collection, Generator, Sequence

from app.api.api_v1.schemas.document import DocumentCreateRequest


class ValidationError(Exception):
    """Base class for import validation errors."""

    def __init__(self, message: str, details: dict):
        self.message = message
        self.details = details


class ImportSchemaMismatchError(ValidationError):
    """Raised when a provided bulk import file fails schema validation."""

    def __init__(self, message: str, details: dict):
        super().__init__(
            message=f"Bulk import file failed schema validation: {message}",
            details=details,
        )


class DocumentsFailedValidationError(ValidationError):
    """Raised when bulk import files fail validation."""

    def __init__(self, message: str, details: dict):
        super().__init__(
            message=f"Document data provided for import failed validation: {message}",
            details=details,
        )


@dataclass
class DocumentValidationResult:
    """Class describing the results of validating individual documents."""

    row: int
    create_request: DocumentCreateRequest
    errors: dict[str, Collection[str]]
    import_id: str


class DocumentGenerator(ABC):
    """Base class for all document sources."""

    @abstractmethod
    def process_source(self) -> Generator[Sequence[DocumentCreateRequest], None, None]:
        """Generate document groups for processing from the configured source."""

        raise NotImplementedError("process_source() not implemented")
