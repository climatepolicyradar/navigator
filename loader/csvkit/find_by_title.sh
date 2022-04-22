#!/usr/bin/env bash
#
# Tips:
# - Use % as wildcard
# - Columns with spaces can be quoted
#
# Example:
# 
# ./csvkit/find_by_title.sh "Federal Climate Protection Act and to change further regulations%" "Frameworks,\"Natural Hazards\",Responses,Instruments,Sectors"

TITLE=${1:-xxx}
SELECT=${2:-*}

echo "Rows where Title = '${TITLE}'"

csvsql --query "\
select \
  ${SELECT} \
from laws_and_policies_16022022
where \
   Title like '${TITLE}'" data/laws_and_policies_16022022.csv
