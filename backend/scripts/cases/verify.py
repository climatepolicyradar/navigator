"""Simple script to verify the csv files in the data folder"""
from pprint import pprint

from data_load import data_load


def verify():
    pass


if __name__ == "__main__":
    data = data_load()
    cases = data["cases"]
    parties = data["parties"]
    documents = data["documents"]
    events = data["events"]

    for id in events.keys():
        pprint(id)
        pprint(events[id])

    verify()
