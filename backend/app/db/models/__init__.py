"""Models.

Some of these tables are lookup tables, i.e. the ones which have a DocumentXXX counterpart.

Values for these lookups can be found here:
https://www.notion.so/climatepolicyradar/External-Pre-Existing-Classifications-0409cd1a01d44362b48b34c24d10cd4c

However, for now we write the values into the lookups as they come from the uploader.
As more sources come online, we'll set up a mapping between the source's term, and our term
(the latter which is currently based on CCLW).


These lookups are global:
- language
- geography
- source
- category
- framework
- hazard
- response (named 'topic' outside the app)

These lookups are source-specific:
- instrument
- sector
"""

from .document import (
    DocumentType,
    Category,
    Document,
    Association,
    Sector,
    DocumentSector,
    Instrument,
    DocumentInstrument,
    Framework,
    DocumentFramework,
    Response,
    DocumentResponse,
    Language,
    DocumentLanguage,
    Hazard,
    DocumentHazard,
    Keyword,
    DocumentKeyword,
    PassageType,
    Passage,
    Event,
    Relationship,
    DocumentRelationship,
)
from .user import User, PasswordResetToken
from .source import Source
from .geography import Geography, GeoStatistics
from .case import (
    LitBody,
    CaseStatus,
    UNFCCCPillars,
    CaseOutcome,
    ClimateAlignmentClass,
    StrategicAlignmentClass,
    Case,
)
from .litiguation import (
    LitCaseKeyword,
    LitCaseInternalLaws,
    LitExternalLaw,
    LitCaseExternalLaws,
    LitPartyType,
    LitSideType,
    LitParty,
    LitCaseParties,
    LitDocument,
    LitEventType,
    LitEvent,
    LitEventDocuments,
)
