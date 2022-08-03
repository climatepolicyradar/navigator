from app.db.models import Source

def populate_source(db):
    # Insert standard sources into source table
    db.add(Source(name="CCLW"))
    db.commit()
