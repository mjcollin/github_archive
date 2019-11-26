#!/bin/bash
year=$1
month=$2

cd data
for d in `seq -f "%02g" 1 31`
do
    for h in `seq -f "%02g" 0 23`
    do
        fn="${year}-${month}-${d}-${h}.json.gz"
        echo "Starting download of $fn"
        wget -nc -q http://data.githubarchive.org/$fn &
    done
    wait
done