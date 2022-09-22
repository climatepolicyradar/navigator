#!/usr/bin/env python3
"""Script that diffs two json outputs from dump_document_details.py comparing the related_documents fields only."""
import sys
import json


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Need to supply two json filenames")
        sys.exit(1)

    data1 = {}
    data2 = {}
    with open(sys.argv[1]) as f1, open(sys.argv[2]) as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    ids1 = [d["id"] for d in data1]
    ids2 = [d["id"] for d in data2]

    if len(ids1) != len(ids2):
        print(f"Differs by number of documents returned {len(ids1)} != {len(ids2)}")
        sys.exit(1)

    if len(ids1) != len(set(ids1)):
        print(f"First file has repeated documents {len(ids1)} != {len(set(ids1))}")
        sys.exit(1)

    if len(ids2) != len(set(ids2)):
        print(f"Second file has repeated documents {len(ids2)} != {len(set(ids2))}")
        sys.exit(1)

    for i, data in enumerate(data1):
        if data1[i]["id"] != data2[i]["id"]:
            print(f"Order differs at {data1[i]['id']} != {data2[i]['id']}")
            sys.exit(1)
        rd1 = [d["document_id"] for d in data1[i]["related_documents"]].sort()
        rd2 = [d["document_id"] for d in data2[i]["related_documents"]].sort()
        if rd1 != rd2:
            print(f"Document {data1[i]['id']} - related docs differs: {rd1} != {rd2}")
            sys.exit(1)

    print(f"OK - Compared {len(ids1)} documents")
