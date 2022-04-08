from typing import Optional

from app.service.lookups import get_language_id, get_language_id_by_part1_code
from app.model import Doc


def get_language_id_for_doc(doc: Doc) -> Optional[int]:
    """Returns the language_id for this doc's language.

    IF the doc's language is null, return None, as the language_id is nullable in the DB.
    If the language_id is not found by country_code (e.g. "eng"), then try to look
    it up by part1_code (e.g "en").
    """
    language_code = doc.doc_language
    if language_code is None:
        return None
    language_code = language_code.lower()
    lang_id = get_language_id(language_code)
    if lang_id is None:
        lang_id = get_language_id_by_part1_code(language_code)
    return lang_id
