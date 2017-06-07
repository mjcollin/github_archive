import os
import sys
import json
import gzip
import glob

data_dir = "data"

def yield_email(d):
    """yeild email and maybe names from a nested dictionary"""
    for k, v in d.items():
        #print(k, v)
        email = False
        if k is "email":
            email = v
        elif isinstance(v, dict) and v.get("email", False):
            email = v["email"]

        if email:
            yield email

        if isinstance(v, dict):
            yield from yield_email(v)
        if isinstance(v, list):
            for i in v:
                yield from yield_email(i)


for fn in glob.glob(os.path.join(data_dir, "*.json.gz")):
    with gzip.open(fn, "rb") as gz:
        for line in gz:
            rec = json.loads(line.decode("utf8"))
            #print(rec)
            for e in yield_email(rec):
                print(e)
            #sys.exit()
