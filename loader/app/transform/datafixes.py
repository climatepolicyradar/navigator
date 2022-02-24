from datetime import datetime
from typing import Dict, Tuple, Optional

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

mapping: Dict[Tuple[str, str], int] = {
    ("BGD", "Bangladesh National Action Plan (NAP) for Reducing Short Lived Climate Pollutants (SLCPs)"): 2018,
    ("ETH", "Climate Resilient Transport Sector Strategy"): 2017,
    ("ETH", "Climate Resilience Strategy: Water and Energy"): 2015,
    ("PAN",
     "Law no 6 of 3 February 1997 on the regulatory and institutional framework of the public electricity service"): 1997,
    ("KOR", "Clean Air Conservation Act (No. 10615)"): 2007,
}


def get_missing_date(policy_name: str, country_code: str) -> Optional[datetime]:
    """Add missing dates to dataset.

    These actions don't have events, and Danny provided some dates:

    Date, Title, Geography
    2018, Bangladesh National Action Plan (NAP) for Reducing Short Lived Climate Pollutants (SLCPs),Bangladesh (BGD)
    2017, Climate Resilient Transport Sector Strategy,Ethiopia (ETH)
    2015, Climate Resilience Strategy: Water and Energy,Ethiopia (ETH)
    1997, Law no 6 of 3 February 1997 on the regulatory and institutional framework of the public electricity service,Panama (PAN)
    2007, Clean Air Conservation Act (No. 10615),South Korea (KOR)
    """
    key = (country_code, policy_name)
    year = mapping.get(key)
    if not year:
        return None
    return datetime(year, 1, 1)
