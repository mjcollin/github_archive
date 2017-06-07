import os
import sys
import json
import gzip
import glob
#import gevent
#from gevent.pool import Pool

#from gevent import monkey
#monkey.patch_socket()

from multiprocessing import Pool

data_dir = "data"

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

def get_emails(fn):
    try:
        with gzip.open(fn, "rb") as gz:
            for line in gz:
                rec = json.loads(line.decode("utf8"))
                #print(rec)
                for p in yield_people(rec):
                    print("{0},{1}".format(p["email"], p.get("name", "Unknown")))
                #sys.exit()
    except:
        print("Error in file {0}".format(fn))

pool = Pool(processes=16)
pool.map(get_emails, glob.glob(os.path.join(data_dir, "*.json.gz")))

