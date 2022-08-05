from app.db.models import Source

def populate_source(db):
    """ Add the single CCLW source.
    """
    db.add(Source(name="CCLW"))
