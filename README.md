# name2id

## How to use?

Add this line to your `~/.bashrc` file on each cluster (Adroit, Della, Perseus, Tiger, Tigressdata and Traverse):

```bash
alias lft='/home/jdh4/bin/name2id'
```

Then look at the help menu:

```
$ name2id -h
```

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
