# name2id

Given the full or partial name of an RC user, `name2id` will find the
corresponding NetID. Fuzzy string matching is used so severe misspellings
of the name still result in a match.

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

The output of the first example is shown below:

```
$ name2id anatolie spitz

            NETID/EMAIL                NAME   DEPT          SPONSOR  PROB
==========================================================================
  anatoly@princeton.edu  Anatoly Spitkovsky  Astro       Spitkovsky  0.69
   nhdiaz@princeton.edu        Natalie Diaz  Astro              Cen  0.69
 alevshin@princeton.edu     Anatoly Levshin                          0.62
 amorozov@princeton.edu     Anatoli Morozov    MAE         Suckewer  0.62
   astatt@princeton.edu       Antonia Statt  PRISM  Panagiotopoulos  0.59
    licao@princeton.edu              Li Cao                          0.57
    nlust@princeton.edu      Nathaniel Lust  Astro           Lupton  0.57
==========================================================================
```

## How does it work?

`getent passwd` is ran on the necessary head nodes (`tigressdata` and others) to capture all RC users. This output is combined into a master file which is stored on each head node. `name2id` uses the fuzzywuzzy package to do the fuzzy string matching. The top 7 most likely results are presented along with their probabilities. The master file is updated three times per day on M-F.



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
