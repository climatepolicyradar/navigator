#!/usr/bin/env bash

TITLE=${1:-xxx}
SELECT=${2:-*}

echo "Rows where Title = '${TITLE}'"

csvsql --query "\
select \
  ${SELECT} \
from laws_and_policies_16022022
where \
   Title like '${TITLE}'" data/laws_and_policies_16022022.csv
