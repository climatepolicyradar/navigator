# Migrate Document Associations to Relationships

This script assumes the following:
1. There is only one `name` and `type` of relationship - called `related`
2. That there can is only a single direction that goes from `document_id_from` to `document_id_to`, i.e. there are no more than a single row with the same `document_id_from` value. This assumption has been tested with:
```
select * from ( 
	SELECT  document_id_from, count(document_id_from)  n
	FROM public.association
	group by document_id_from
) as t where t.n > 1;

select * from ( 
	SELECT  document_id_to, count(document_id_to)  n
	FROM public.association
	group by document_id_to 
) as t where t.n > 1;
```

