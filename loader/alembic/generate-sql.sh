#!/usr/bin/env bash

alembic upgrade $(alembic history | head -n1 | awk '{print $1}'):head --sql
echo
alembic downgrade head:-1 --sql
