import os
import sys
import json
import gzip
import glob
from collections import OrderedDict
#import gevent
#from gevent.pool import Pool

#from gevent import monkey
#monkey.patch_socket()

from multiprocessing import Pool

data_dir = "data"
file_pattern = "2016-10-01-2.json.gz"
ignore_events = set([
    "CreateEvent",
    "DeleteEvent",
    "GollumEvent",
    "IssueCommentEvent",
    "IssuesEvent",
    "MemberEvent",
    "PublicEvent",
    "WatchEvent"])

def yield_people(d):
    """yeild email and maybe names from a nested dictionary"""
    for k, v in d.items():
        person = {}

        if k is "email":
            person["email"] = v
        elif isinstance(v, dict) and v.get("email", False):
            person["email"] = v["email"]
            if v.get("name", False):
                person["name"] = v["name"]
            elif v.get("login", False):
                person["name"] = v["login"]

        if person:
            yield person

        if isinstance(v, dict):
            yield from yield_people(v)
        if isinstance(v, list):
            for i in v:
                yield from yield_people(i)

def yield_dicts(fn):
    try:
        with gzip.open(fn, "rb") as gz:
            for line in gz:
                yield json.loads(line.decode("utf8"))
    except:
        print(f"Error in file {fn}")


def get_emails(fn):
    for d in yield_dicts(fn):
        #print(d)
        for p in yield_people(d):
            #if args.csv:
            print(f"{p['email']},{p.get('name', 'Unknown')}")

def get_main_author(d):
    retval = {"name": "", "email": ""}
    commiters = {}
    commits = d["payload"].get('commits', [])
    for c in commits:
        people = yield_people(c)
        for p in people:
            return p
    return retval


def print_event(d):
    row = OrderedDict()
    row["id"] = d.get("id", "")
    row["type"] = d.get("type", "")
    row["login"] = d["actor"]["login"] if d.get("actor") else ""
    row["repo"] = d["repo"]["name"] if d.get("repo") else ""
    row["push_id"] = d["payload"].get("push_id", "")
    row["created_at"] = d.get("created_at", "")
    # }
    # row = {**row, **get_main_author(d)}
    #print(json.dumps(row))
    if row["type"] not in ignore_events:
        print(",".join([str(v) for v in row.values()]))

def get_events(fn):
    for d in yield_dicts(fn):
        print_event(d)

def main(args):
    fns = glob.glob(os.path.join(data_dir, file_pattern))

    multi_threaded = True
    if multi_threaded:
        pool = Pool(processes=10)
        pool.map(get_events, fns)
    else:
        for fn in fns:
            get_emails(fn)


if __name__ == '__main__':

    main("asdf")
