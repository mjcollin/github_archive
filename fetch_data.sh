#!/bin/bash

cd data
for i in `seq 0 23` ; do wget -q http://data.githubarchive.org/2017-05-{01..31}-${i}.json.gz & done;
