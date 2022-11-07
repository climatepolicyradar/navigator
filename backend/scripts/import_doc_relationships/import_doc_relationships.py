#!/usr/bin/env python3

from app.db.session import SessionLocal

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

    for group in groups:
        name = f"imported_relation_{group[0]}"
        document_ids = group[1]
        print(f"Creating relationship '{name}' for ids: {document_ids}")

    # Do the biz
    db.commit()
