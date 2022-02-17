import datetime as dt
import re

from dateutil.parser import parse

DEFAULT_POLICY_DATE = dt.date(1900, 1, 1)


def clean_url(url):
    """Remove additional date strings which are erroneously present in some of the CCLW urls"""

    url = re.sub('\([0-9]+\-[a-zA-Z]{3,}\-[0-9]+\)', '', url)

    return url


def split_and_merge_urls(doc_urls, sep):
    """Splits a given string of urls, and returns a list of matching urls.

    Merges cases where the comma is included in the url and not as a separator.

    TODO this code was copied from the prototype Jupyter notebook, but has to be
    reconsidered for non-http URLs (e.g. FTP, torrent links, etc)
    """
    doc_urls = doc_urls.split(sep)
    # Iterate through the returns urls and merge each element with the previous one if it does not start with https?://
    merged_doc_urls = []
    for u_ix, u in enumerate(doc_urls):
        u = u.strip()
        if u[0:4] == 'http':
            merged_doc_urls.append(u)
        elif u_ix > 0 and u[0:4] != 'http':
            if len(merged_doc_urls) > 0 and len(u) > 0:
                merged_doc_urls[-1] = merged_doc_urls[-1] + u

    # Drop duplicate urls
    merged_doc_urls = list(set(merged_doc_urls))

    return merged_doc_urls


def get_urls(dataframe, policy_id=None, sep=';', sub_sep=None, url_sep=','):
    country_code = dataframe['country_code']
    policy_name = dataframe['policy_name']
    doc_list = dataframe['document_list']
    description = dataframe['policy_description']

    docs = []
    if type(doc_list) == str:
        for u in doc_list.split(sep):
            if sub_sep is not None:
                u_info = u.split(sub_sep)
                doc_name = u_info[0]
                doc_url = clean_url(u_info[1])
                # Now try splitting on commas as sometimes there are multiple urls separated by commas
                doc_url = split_and_merge_urls(doc_url, url_sep)
                doc_language = u_info[2] if len(u_info[2]) > 0 else None
            else:
                doc_name = ''
                doc_url = split_and_merge_urls(u, url_sep)
                doc_language = None

            # Now iterate through the urls for this document and add all the urls we have found
            for u in doc_url:
                # Add encoded url
                doc = {}
                doc['policy_id'] = policy_id
                doc['country_code'] = country_code
                doc['policy_name'] = policy_name
                doc['doc_name'] = doc_name
                doc['language'] = doc_language
                doc['doc_url'] = u
                doc['description'] = description
                doc["events"] = dataframe["events"]
                docs.append(doc)
    return docs


def extract_date(val: str):
    if not val or not isinstance(val, str):
        return None
    date_str = val.split('|')[0]
    if date_str:
        date = parse(date_str)
        return date
    return DEFAULT_POLICY_DATE
