import logging
import re
from datetime import datetime
from html.parser import HTMLParser
from io import StringIO
from typing import Tuple, List, Optional

from dateutil.parser import parse

from app.loaders.loader.transform.datafixes import get_missing_date
from app.mapping import CCLWActionType
from app.model import Key, Doc, PolicyData

DEFAULT_POLICY_DATE = datetime(1900, 1, 1)

logger = logging.getLogger(__file__)


def clean_url(url):
    """Remove additional date strings which are erroneously present in some of the CCLW urls."""

    url = re.sub(r"([0-9]+-[a-zA-Z]{3,}-[0-9]+)", "", url)

    return url


def split_and_merge_urls(doc_urls, sep):
    """Split a given string of urls, and returns a list of matching urls.

    Merges cases where the comma is included in the url and not as a separator.

    TODO this code was copied from the prototype Jupyter notebook, but has to be
    reconsidered for non-http URLs (e.g. FTP, torrent links, etc)
    """
    doc_urls = doc_urls.split(sep)
    # Iterate through the returns urls and merge each element with the previous one if it does not start with https?://
    merged_doc_urls = []
    for u_ix, u in enumerate(doc_urls):
        u = u.strip()
        if u[0:4] == "http":
            merged_doc_urls.append(u)
        elif u_ix > 0 and u[0:4] != "http":
            if len(merged_doc_urls) > 0 and len(u) > 0:
                merged_doc_urls[-1] = merged_doc_urls[-1] + u

    # Drop duplicate urls
    merged_doc_urls = list(set(merged_doc_urls))

    return merged_doc_urls


def prune(lst: List[str]) -> List:
    return list(filter(None, lst))


def get_policy_data(
    dataframe, sep=";", sub_sep=None, url_sep=","
) -> Optional[Tuple[Key, PolicyData]]:

    policy_name = dataframe["policy_name"]
    country_code = dataframe["country_code"]
    policy_category = CCLWActionType[dataframe["policy_category"]].value
    document_type = dataframe["document_type"]
    events = prune(dataframe["events"].split("||"))
    sectors = prune(dataframe["sectors"].split(","))
    instruments = prune(dataframe["instruments"].split(";"))
    frameworks = prune(dataframe["frameworks"].split(","))
    responses = prune(dataframe["responses"].split(","))
    hazards = prune(dataframe["hazards"].split(","))

    policy_date: Optional[datetime] = extract_date(dataframe["events"])
    if not policy_date:
        policy_date = get_missing_date(policy_name, country_code)
    if not policy_date:
        logger.warning(
            f"Found no date for policy policy_name={policy_name}, policy_category={policy_category}, country_code={country_code}"
        )
        return

    key = Key(
        policy_date=policy_date,
        country_code=country_code,
        policy_name=policy_name,
        policy_category=policy_category,
    )

    doc_list = dataframe["document_list"]

    if type(doc_list) == str:
        docs: List[Doc] = []
        for u in doc_list.split(sep):
            if sub_sep is not None:
                u_info = u.split(sub_sep)
                doc_name = u_info[0]
                doc_urls = clean_url(u_info[1])
                # Now try splitting on commas as sometimes there are multiple urls separated by commas
                doc_urls = split_and_merge_urls(doc_urls, url_sep)
                doc_language = u_info[2] if len(u_info[2]) > 0 else None
            else:
                doc_name = ""
                doc_urls = split_and_merge_urls(u, url_sep)
                doc_language = None

            # Now iterate through the urls for this document and add all the urls we have found
            for doc_url in doc_urls:
                doc = Doc(
                    doc_name=doc_name,
                    doc_languages=[doc_language],
                    doc_url=ensure_safe(doc_url),
                    document_type=document_type,
                    events=events,
                    sectors=sectors,
                    instruments=instruments,
                    frameworks=frameworks,
                    responses=responses,
                    hazards=hazards,
                )
                docs.append(doc)

        if docs:
            data = PolicyData(
                policy_date=policy_date,
                country_code=country_code,
                policy_name=policy_name,
                policy_category=policy_category,
                policy_description=strip_tags(dataframe["policy_description"]),
                docs=docs,
            )
            return key, data
        else:
            logger.warning(f"Found no docs for policy {key}")


def extract_date(val: Optional[str]) -> Optional[datetime]:
    if not val or not isinstance(val, str):
        return None
    date_str = val.split("|")[0]
    if date_str:
        date = parse(date_str)
        return date
    return DEFAULT_POLICY_DATE


def ensure_safe(url: str) -> str:
    """Ensure a URL is safe.

    Some documents use http, not https. Instead of just ignoring those,
    we'll try download a doc securely, if possible.
    """
    if "https://" not in url:
        url = url.replace("http://", "https://")
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
