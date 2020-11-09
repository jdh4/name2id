# name2id

## How to use it?

Add this line to your `~/.bashrc` file on each cluster (Adroit, Della, Perseus, Tiger, Tigressdata and Traverse):

```bash
alias name2id='/home/jdh4/bin/name2id'
```

Then look at the help menu:

```
$ name2id -h

Given the full or partial name of an RC user, name2id will find the
corresponding NetID. Fuzzy string matching is used so severe misspellings
of the name still result in a match.

Examples:
       $ name2id anatolie spitz
       $ name2id debeneti
       $ name2id red maxell
       $ name2id irene
```

## How does it work?

`getent passwd` is ran on the necessary head hodes to capture all RC users. every cluster every four hours M-F. This output is combined into a master file. That file is sent back out to each head node. The software using the fuzzywuzzy package to do the fuzzy string matching. Only the top 7 results are presented along with their probabilities.

It is only useful when you are looking for the NetID of someone who already has an RC acount. There are roughly 3400 users in the master file.

## When is it useful?

It is useful when:

+ account requests only mention the PI by name
+ RCU/DCU users submit a ticket using their non-PU email

## getent passwd vs. ls /home

(8/22)
```
-- tiger --
$ getent passwd | wc -l
2179
$ ls /home | wc -l
971

-- tigressdata --
$ getent passwd | wc -l
2134
$ ls /home/| wc -l
2043

-- della --
$ getent passwd | wc -l
2178
$ ls /home | wc -l
1253

-- traverse --
$ getent passwd | wc -l
84
$ ls /home | wc -l
147
```

```
(11/9) -- traverse --
$ getent passwd | wc -l
2327
$ ls /home | wc -l
160
```

```
diff -y <(ls /home | sort | uniq) <(getent passwd | cut -d':' -f 1 | sort | uniq)
```

```
$ getent passwd | cut -d ':' -f 7 | sort | uniq
/bin/bash
/bin/csh
/bin/sh
/bin/sync
/bin/tcsh
/bin/zsh
/sbin/halt
/sbin/nologin
/sbin/shutdown
/usr/bin/zsh
```
