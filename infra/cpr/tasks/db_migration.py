from dataclasses import dataclass
from typing import List


@dataclass
class DBMigrationTaskInput:  # noqa:D101
    cluster_arn: str
    task_definition_arn: str
    subnet_ids: List[str]
    security_group_ids: List[str]


def db_migration_task(input: DBMigrationTaskInput):
    pass
