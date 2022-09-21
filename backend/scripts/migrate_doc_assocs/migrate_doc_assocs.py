#!/usr/bin/env python3

import sys
from app.db.models import Association, Relationship, DocumentRelationship
from app.db.session import SessionLocal
from sqlalchemy.orm import Session


def _convert_associations_to_relationship(db: Session, id: int):
    # Create the new relationship of this set
    new_relationship = Relationship(
        type="related",
        name="related",
        description="Migrated from CCLW document group",
    )
    db.add(new_relationship)
    db.commit()
    db.refresh(new_relationship)

    def add_doc_relationship(doc_id: int):
        db.add(
            DocumentRelationship(
                document_id=doc_id, relationship_id=new_relationship.id
            )
        )

    # add the parent to this new relationship (the "to" part of the association)
    add_doc_relationship(id)

    # add the child documents (any "from" document id with a matching "to")
    [
        add_doc_relationship(to_id)
        for to_id, in db.query(Association.document_id_from).filter(
            Association.document_id_to == id
        )
    ]
    db.commit()


if __name__ == "__main__":
    print("Migrating document associations to relationships...")
    db = SessionLocal()

    all_associations = db.query(Association).all()
    print(f"...found {len(all_associations)} associations...")

    # Get all distinct document ids in the "to" part of the relationship
    to_docs = db.query(Association.document_id_to).distinct().all()
    print(f"...found {len(to_docs)} documents with associations...")
    n_expected_document_relationships = len(all_associations) + len(to_docs)

    for (doc_id,) in to_docs:
        _convert_associations_to_relationship(db, doc_id)

    # validation
    n_actual_document_relationships = db.query(DocumentRelationship).count()

    sys.exit(
        0 if n_actual_document_relationships == n_expected_document_relationships else 1
    )
