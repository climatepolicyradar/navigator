from dataclasses import dataclass
from pandas import DataFrame


@dataclass()
class IngestData:
    policies: DataFrame
    docs: DataFrame
    targets: DataFrame
    policies_fe: DataFrame
