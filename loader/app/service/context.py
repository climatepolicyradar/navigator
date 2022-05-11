from dataclasses import dataclass

import httpx
from sqlalchemy.orm import Session


@dataclass
class Context:
    """A context of all internal services for use by the loader applications."""

    db: Session
    client: httpx.AsyncClient
