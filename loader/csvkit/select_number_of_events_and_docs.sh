#!/usr/bin/env bash

csvsql --query "\
select \
  (length(Documents) - length(replace(Documents, 'http', '')))/length('http') as doc_count, \
  (length(Events) - length(replace(Events, '||', '')))/length('||') as event_count, \
  Title as name \
from laws_and_policies_16022022
where \
  Events is not null and \
  Documents is not null \
  group by Title \
  order by event_count desc, doc_count desc, name " data/laws_and_policies_16022022.csv
