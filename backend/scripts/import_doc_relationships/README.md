# Import document relationships 

## Assumptions

- Documents are already in the database

## Usage

1. Run `nav-stack-connect.sh` from the [navigator-scripts](https://github.com/climatepolicyradar/navigator-scripts) repository, [read the docs](https://github.com/climatepolicyradar/navigator-scripts/blob/ffe777ba9f44d4570c3d8923a7fd5071f9aa4f49/docs/nav-stack-connect.md?plain=1#L1), ensuring:
	- you have set `AWS_PROFILE` correctly and selected the correct pulumi stack
	- sourced the correct vars file: `source ~/.aws/${AWS_PROFILE}_vars.sh`

2. From the `backend` folder in the repository run:
```bash
PYTHONPATH=$PWD python scripts/import_doc_relationships/import_doc_relationships.py
```

## SQL

The SQL used in this script is a little "postgres" ish ... it may use a few functions you're unfamiliar with:

```
SELECT * FROM (
	SELECT (string_to_array(import_id, '.'))[3] AS grouping_id, json_agg(id) as id_list, count(id) as len 
		FROM document 
		GROUP BY grouping_id
	) AS T where T.len > 1;
```

Salient functions:

- `string_to_array` - this will split the argument (in this case `import_id`) similar to `string.split()` in python
- The import id is split on a period '.' and the 3rd element is the one we are going to group by, hence the name `grouping_id`
- `json_agg` is the aggregation function that is used when the data is grouped over `grouping_id` and it creates a json array of document ids to be grouped.
- Finally for completion we only select groups with more than one document in them and this will result in a dataset that is lists the relationships to make with the containing document ids :
 
 ```
  grouping_id |            id_list             | len 
-------------+--------------------------------+-----
 10007       | [3451, 3117, 3452]             |   3
 10016       | [3124, 3123]                   |   2
 10032       | [3199, 3198]                   |   2
 10039       | [3924, 3923]                   |   2
 10049       | [3947, 3948]                   |   2
 10060       | [3969, 3970]                   |   2
 10061       | [3823, 3824]                   |   2
 10072       | [3899, 3900]                   |   2
 10087       | [3352, 3353]                   |   2
 10099       | [3355, 3356, 3354]             |   3
 10102       | [3428, 3427]                   |   2
 10108       | [3245, 3246]                   |   2
 10109       | [3371, 3372, 3373]             |   3
 10115       | [3834, 3833]                   |   2

 ```
