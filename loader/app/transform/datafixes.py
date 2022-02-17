import datetime as dt

from pandas import DataFrame

mappings = [
    {
        'country_code': 'BGD',
        'policy_name': 'Bangladesh National Action Plan (NAP) for Reducing Short Lived Climate Pollutants (SLCPs)',
        'year': 2018,
    },
    {
        'country_code': 'ETH',
        'policy_name': 'Climate Resilient Transport Sector Strategy',
        'year': 2017,
    },
    {
        'country_code': 'ETH',
        'policy_name': 'Climate Resilience Strategy: Water and Energy',
        'year': 2015,
    },
    {
        'country_code': 'PAN',
        'policy_name': 'Law no 6 of 3 February 1997 on the regulatory and institutional framework of the public electricity service',
        'year': 1997,
    },
    {
        'country_code': 'KOR',
        'policy_name': 'Clean Air Conservation Act (No. 10615)',
        'year': 2007,
    },
]


def add_missing_dates(policies: DataFrame):
    """Add missing dates to dataset.

    These actions don't have events, and Danny provided some dates:

    Date, Title, Geography
    2018, Bangladesh National Action Plan (NAP) for Reducing Short Lived Climate Pollutants (SLCPs),Bangladesh (BGD)
    2017, Climate Resilient Transport Sector Strategy,Ethiopia (ETH)
    2015, Climate Resilience Strategy: Water and Energy,Ethiopia (ETH)
    1997, Law no 6 of 3 February 1997 on the regulatory and institutional framework of the public electricity service,Panama (PAN)
    2007, Clean Air Conservation Act (No. 10615),South Korea (KOR)
    """

    dt.date(1900, 1, 1)

    for mapping in mappings:
        policies.loc[
            (policies['country_code'] == mapping['country_code']) & (
                    policies['policy_name'] == mapping['policy_name'])] = dt.date(mapping['year'], 1, 1)
