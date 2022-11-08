# Import document postfixes 

## Assumptions

- Documents are already in the database

## Usage

1. Run `nav-stack-connect.sh` from the [navigator-scripts](https://github.com/climatepolicyradar/navigator-scripts) repository, [read the docs](https://github.com/climatepolicyradar/navigator-scripts/blob/ffe777ba9f44d4570c3d8923a7fd5071f9aa4f49/docs/nav-stack-connect.md?plain=1#L1), ensuring:
	- you have set `AWS_PROFILE` correctly and selected the correct pulumi stack
	- sourced the correct vars file: `source ~/.aws/${AWS_PROFILE}_vars.sh`

2. From the `backend` folder in the repository run:
```bash
PYTHONPATH=$PWD python scripts/import_doc_postfix/import_doc_postfix.py <csv_file>
```