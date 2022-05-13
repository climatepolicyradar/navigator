import logging
from datetime import datetime
from html.parser import HTMLParser
from io import StringIO
from typing import Tuple, List, Optional

from dateutil.parser import parse, ParserError
from pandas import DataFrame

from app.mapping import CCLWActionType
from app.model import Key, Doc, PolicyData, Event

DEFAULT_POLICY_DATE = datetime(1900, 1, 1)

logger = logging.getLogger(__file__)


def prune(lst: List[str]) -> List:
    return [it.strip() for it in filter(None, lst)]


def extract_events(events_str: str) -> List[Event]:
    events = []
    for event in prune(events_str.split(";")):
        parts = event.split("|")
        date_str = parts[0]
        event_date = datetime.strptime(date_str, "%d/%m/%Y")
        event_name = parts[1]
        events.append(Event(name=event_name, date=event_date))
    return events


def get_policy_data(
    policy_id: str,
    group_dataframe,
) -> Optional[Tuple[Key, PolicyData]]:

    country_code = get_country_code(group_dataframe)

    key = Key(
        country_code=country_code,
        policy_name=policy_id,
        policy_date=None,
        policy_category=None,
    )

    docs = []
    for _idx, dataframe in group_dataframe.iterrows():

        document_name = dataframe["document_name"]
        document_description = dataframe["document_description"]
        document_url = dataframe["document_url"]
        document_language = dataframe["document_language"]
        document_country_code = dataframe["country_code"]
        document_category = CCLWActionType[dataframe["category"]].value
        document_type = dataframe["document_type"]
        events = extract_events(dataframe["events"])
        sectors = prune(dataframe["sectors"].split(";"))
        instruments = prune(dataframe["instruments"].split(";"))
        frameworks = prune(dataframe["frameworks"].split(";"))
        responses = prune(dataframe["responses"].split(";"))
        hazards = prune(dataframe["hazards"].split(";"))
        keywords = prune(dataframe["keywords"].split(";"))
        year = dataframe["document_year"]

        if document_country_code != country_code:
            logger.warning(
                f"Related documents have different geographies, document_name={document_name}, "
                f"policy_name={policy_id}, document_category={document_category}, "
                f"country_code={country_code}"
            )

        if year:
            publication_date = datetime(int(year), 1, 1)
        else:
            publication_date = extract_date(dataframe["events"])

        doc = Doc(
            doc_name=document_name,
            doc_description=document_description,
            doc_languages=[document_language],
            doc_url=parse_url(document_url),
            document_type=document_type,
            publication_date=publication_date,
            document_category=document_category,
            events=events,
            sectors=sectors,
            instruments=instruments,
            frameworks=frameworks,
            responses=responses,
            hazards=hazards,
            keywords=keywords,
        )

        docs.append(doc)

    if docs:
        data = PolicyData(
            policy_date=None,
            policy_category=None,
            policy_description=None,
            country_code=country_code,
            policy_name=policy_id,
            docs=docs,
        )
        return key, data
    else:
        logger.warning(f"Found no docs for policy {key}")


def get_country_code(df: DataFrame):
    """Returns the first country_code.

    All grouped dataframes should have the same country code,
    as related policy documents usually span a common geography.
    """
    return df.iloc[0]["country_code"]


def extract_date(val: Optional[str]) -> datetime:
    """Extract the first date from possible events.

    Defaults to DEFAULT_POLICY_DATE if there are any issues:
    - missing events
    - broken events
    """
    if not val or not isinstance(val, str):
        return DEFAULT_POLICY_DATE

    try:
        date_str = val.split("|")[0]
    except IndexError:
        logger.warning(f"Event could not be parsed: {val}")
        return DEFAULT_POLICY_DATE

    if date_str:
        try:
            date = parse(date_str)
            return date
        except ParserError:
            logger.warning(f"Date could not be parsed: {date_str}")
            return DEFAULT_POLICY_DATE

    return DEFAULT_POLICY_DATE


def parse_url(url: str) -> str:
    """Parse a document URL.

    - convert http to https
    - Remove any delimiters (a hang-over from the original CSV)
    """

    url = url.replace("http://", "https://")
    url = url.split("|")[0]
    return url


class MLStripper(HTMLParser):
    """Strips HTML from strings."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):  # noqa:D102
        self.text.write(d)

    def get_data(self):  # noqa:D102
        return self.text.getvalue()


def strip_tags(html: str) -> str:
    s = MLStripper()
    s.feed(html)
    return s.get_data()
