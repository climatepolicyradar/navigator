#!/usr/bin/env python3

from datetime import datetime
from app.db.models.document import DocumentRelationship, Relationship
from app.db.session import SessionLocal


def create_relationship_with_docs(db, cclw_group_id, document_ids):
    name = f"imported_relation_{cclw_group_id}"
    print(
        f"Creating relationship called '{name}' for {cclw_group_id} with doc ids: {document_ids}..."
    )

    relationship = Relationship(
        name=name,
        type="SYSTEM",
        description=f"CCLW group ID {cclw_group_id}, imported at {datetime.now()}",
    )
    db.add(relationship)
    db.flush()

    for doc_id in document_ids:
        link = DocumentRelationship(document_id=doc_id, relationship_id=relationship.id)
        db.add(link)
        print(f"... added {doc_id} to relationship {relationship.id}")


if __name__ == "__main__":
    print("Importing document relationships...")
    db = SessionLocal()
    groups = db.execute(
        """
    SELECT * FROM (
        SELECT (string_to_array(import_id, '.'))[3] AS grouping_id, json_agg(id) as id_list, count(id) as len
            FROM document
            GROUP BY grouping_id
        ) AS T where T.len > 1;
    """
    ).all()

    try:
        with db.begin_nested():
            for group in groups:
                create_relationship_with_docs(db, group[0], group[1])
        db.commit()
    except Exception as e:
        print(e)
        print("Error - nothing committed to the database")
