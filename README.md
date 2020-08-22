# name2id

## Installation

Clone the fuzzywuzzy directory (do not install since it is pure Python). Correct path to fuzzywuzzy in name2id if necessary.

The git repo is `/tigress/jdh4/python-devel/name2id` where development should be done. The executable should be copied to `/tigress/jdh4/python-utilities` where it can be called.

## getent passwd vs. ls /home

(8/22)
-- tiger --
$ getent passwd | wc -l
2179
$ ls /home | wc -l
971

