#!/bin/bash
year=$1
month=$2

cd data
for i in `seq 0 23` ; do wget -nc -q http://data.githubarchive.org/${year}-${month}-{01..31}-${i}.json.gz & done;
wait
