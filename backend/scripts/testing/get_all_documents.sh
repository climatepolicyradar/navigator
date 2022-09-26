#!/bin/bash

#
# This is a pre-cursor to the python scripts - but left here for reference
#
get_related_docs() {
    DOCID=$1
    echo -n "${DOCID}, "
    curl -s "http://localhost:8000/api/v1/documents/${DOCID}" \
        -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:105.0) Gecko/20100101 Firefox/105.0' \
        -H 'Accept: application/json, text/plain, */*' \
        -H 'Accept-Language: en-US,en;q=0.5' \
        -H 'Accept-Encoding: gzip, deflate, br' \
        -H 'Origin: http://localhost:3000' \
        -H 'DNT: 1' \
        -H 'Connection: keep-alive' \
        -H 'Referer: http://localhost:3000/' \
        -H 'Sec-Fetch-Dest: empty' \
        -H 'Sec-Fetch-Mode: cors' \
        -H 'Sec-Fetch-Site: same-site' \
        | jq 
        # | jq "{id} + (.related_documents[] | {document_id})"
    echo ""
}

for id in `cat docids.csv`
do
    get_related_docs $id
done