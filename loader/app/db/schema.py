from dataclasses import dataclass


@dataclass
class AssociationSchema:
    """A remote association, to be posted to backend.

    TODO move to common schemas.
    """

    document_id_to: int
    document_id_from: int
    name: str
    type: str
