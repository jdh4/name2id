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

`getent passwd` is ran on the necessary head nodes (`tigressdata` and others) to capture all RC users. This output is combined into a master file which is stored on each head node. The master file is updated three times per day M-F. `name2id` uses the `fuzzywuzzy` package for fuzzy string matching. The top seven most likely results are presented along with their probabilities.



## When is it useful?

`name2id` is particualrly useful when:

+ account requests mention the PI by name but don't include email
+ RCU/DCU users submit a ticket using their non-PU email
+ you need a user's NetID but don't know how to spell their name
