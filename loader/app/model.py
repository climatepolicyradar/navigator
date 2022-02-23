from dataclasses import dataclass

from pandas import DataFrame


@dataclass()
class IngestData:
    """Represents data coming from extraction phase."""

    policies: DataFrame
    docs: DataFrame
    targets: DataFrame
    policies_fe: DataFrame
