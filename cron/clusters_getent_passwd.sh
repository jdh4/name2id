#!/bin/bash

cd /tigress/jdh4/python-devel/name2id/cron

# pull in output of "getent passwd" from each cluster to here
for cluster in adroit della perseus tigressdata traverse
do
  ssh    jdh4@${cluster}.princeton.edu "getent passwd > /home/jdh4/bin/cron/${cluster}_getent.txt 2>/dev/null"
  scp -q jdh4@${cluster}.princeton.edu:/home/jdh4/bin/cron/${cluster}_getent.txt . 2>/dev/null
done
getent passwd > ./tiger_getent.txt 2>/dev/null

# combine results from each cluster
/usr/licensed/anaconda3/2020.7/bin/python combine_getent.py 2>/dev/null

# push out master file to each cluster
for cluster in adroit della perseus tigressdata traverse
do
  scp -q combined_getent.csv jdh4@${cluster}.princeton.edu:/home/jdh4/bin/cron 2>/dev/null
done
cp combined_getent.csv /home/jdh4/bin/cron 2>/dev/null
