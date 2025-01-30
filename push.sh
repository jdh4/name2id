#!/bin/bash

# della
cp name2id /home/jdh4/bin

# other clusters
for cluster in adroit tiger3 stellar-intel
do
  echo ${cluster}
  scp name2id jdh4@${cluster}.princeton.edu:/home/jdh4/bin
  echo
done
