#!/bin/bash

# tiger
cp name2id /home/jdh4/bin

# other clusters
for cluster in adroit della perseus tigressdata traverse stellar-intel
do
  echo ${cluster}
  scp name2id jdh4@${cluster}.princeton.edu:/home/jdh4/bin
  echo
done
