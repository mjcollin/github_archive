# Running

Downloaded all of 2017 with:

```
mkdir data
for i in {01..12} ; do ./fetch_data.sh 2017 $i; done;
```


Pulled out all emails (and some names) with:

```
python3 get_emails.py > data/all_emails_2017.csv
```

Summarized with:

```
cat data/all_emails_2017.csv | grep 'ufl.edu,' | sort | uniq -c > data/uf_emails_names_2017.txt
cat data/all_emails_2017.csv | grep 'ufl.edu,' | awk -F ',' '{print $1}' | sort | uniq -c > data/uf_emails_2017.txt
cat data/uf_emails_2017.txt | awk '{sum+=$1} END {print sum}'
```


# Results 

Runtime ~ 25 minutes on 128 threads.

~170 GB of .json.gz data for 2017

338 yeilded activities w/ emails

1519 *@*ufl.edu emails and name combinations
1177 *@*ufl.edu emails (ignoring name string)
67256 events from *@*ufl.edu emails

Emails in this data are:
1. Only associated with commits to public repositories, private repos are not included
1. Come from the configuration of the git client. People might have their machine set to
use a personal email address when making commit messages.
1. Don't reflect any of a user's potentially multiple email addresses at Github

