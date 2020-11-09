#!/usr/licensed/anaconda3/2020.7/bin/python

# The output of "getent passwd" is combined and filtered for the
# different clusters. Adroit is handled as a special case since
# it does not contain name_sponsor info for most users.

# The number of entries in the resulting file should be
# minimized to speed-up the search.

import pandas as pd

def fix_lastname_first_comma(full_name):
  parts = full_name.split()
  if (parts[0].endswith(',')):
    return ' '.join(parts[1:] + [parts[0][:-1]])
  else:
    return full_name

def remove_middle_initial(full_name):
  parts = full_name.split()
  cnt = len(parts)
  if (cnt > 2):
    for i in range(1, cnt - 1):
      if (parts[i].endswith('.') and (len(parts[i]) == 2)) or len(parts[i]) == 1:
        _ = parts.pop(i)
      return ' '.join(parts)
  else:
    return full_name

def format_sponsor(s):
  # extract last name from sponsor (taken from dossier.py)
  if pd.isna(s): return ''
  names = list(filter(lambda x: x not in ['Jr.', 'II', 'III', 'IV'], s.split()))
  if len(names) == 2:
    if len(names[1]) > 1: return names[1]
    else: return s
  elif (len(names) > 2):
    idx = 0
    while (names[idx].endswith('.') and (idx < len(names) - 1)):
      idx += 1
    names = names[idx:]
    e = ''.join([str(int(name.endswith('.'))) for name in names])
    if '1' in e: return ' '.join(names[e.index('1') + 1:])
    else: return names[-1]
  else:
    return s

def extract_name(s):
  dept = {'AOS', 'AS-OIT', 'Astro', 'CBE', 'CEE', 'CS', 'CSES', 'CSML', 'Chemistry',
          'EE', 'EEB', 'Economics', 'Energy Systems Analysis', 'GEO', 'Genomics', 'History',
          'IAS', 'MAE', 'Math', 'MolBio', 'OIT', 'ORFE', 'PACM', 'PCTS', 'PICSciE', 'PNI',
          'PPPL', 'PRISM', 'Physics', 'Politics', 'Psychology', 'RC', 'SPIA', 'Sociology'}

  import re
  phone = re.compile(r'\d\d\d-\d\d\d-\d\d\d\d')
  has_number = re.compile(r'\d\d\d')
  if s.endswith(',,,') or s.endswith(',,'):
    # Anna Chorniy,,,
    # Menghang Wang,,
    return [s.split(",")[0], None, None]
  elif s.count(",") == 3 and bool(phone.search(s)):
    # Christine M. McCoy,110 Peretsman Scully Hall,609-258-4442,
    return [s.split(',')[0], None, None]
  elif s.count(",") > 1 and any([item in dept for item in s.split(",")]):
    # Alicia Chen,Politics,Jacob N. Shapiro
    # Park, Noel R.,Genomics,Shawn M. Davidson
    # Hossein Valavi,PNI,Peter J. Ramadge,Naveen Verma
    parts = [item.strip() for item in s.split(",")]
    parts_in_dept = [item in dept for item in parts]
    idx = parts_in_dept.index(True)
    mydept = parts[idx]
    mysponsor = ",".join(parts[idx + 1:])  # 2 sponsors in some cases
    myname = ", ".join(parts[:idx])
    if "," in myname: myname = fix_lastname_first_comma(myname)
    return [myname, mydept, mysponsor]
  elif s.count(",") > 1 and (bool(has_number.search(s)) or s.endswith(',NONE,')):
    # Jonathan T. Wilding,317 87 Prospect Avenue,8-6025,
    # Prasad S. Lakkaraju,101 Frick Lab,NONE,
    return [s.split(',')[0], None, None]
  else:
    # Margaret Martonosi, EE475 TA
    return [s.split(',')[0], None, None]

files = ['tigressdata_getent.txt', 'adroit_getent.txt', 'della_getent.txt', \
         'perseus_getent.txt', 'tiger_getent.txt', 'traverse_getent.txt']

df = pd.DataFrame()
for f in files:
  tmp = pd.read_csv(f, header=None, delimiter=':')
  tmp['cluster'] = 'adroit' if 'adroit' in f else 'other'
  df = df.append(tmp)
df.columns = ['NETID', 'sym', 'uid', 'gid', 'name_sponsor', \
              'home', 'login', 'cluster']

# next lines used for understanding the raw values in the dataframe
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
#pd.set_option('expand_frame_repr', True)
#pd.set_option('max_colwidth', 75)
#pd.set_option('display.width', 200)
#df.reset_index(inplace=True, drop=True)
#print(df[df.name_sponsor.str.contains("Computer Support", na=False)])
#print(df.shape)
#print(df[df.cluster == "adroit"].drop_duplicates().sort_values(by='netid', ascending=True))
#print(df[~df.home.str.contains("home", na=False)].drop_duplicates().sort_values(by='netid', ascending=True))
#print(df[df.name_sponsor.notna() & (~df.name_sponsor.str.contains(',', na=False))].to_string())
#no_shell = ['/sbin/halt', '/sbin/nologin', '/sbin/nolgin', '/sbin/shutdown', '/bin/sync']
#df = df[~df.login.isin(no_shell)]

df = df[['NETID', 'name_sponsor', 'home', 'cluster']]
df = df[df.name_sponsor.str.contains(',', na=False) & df.home.str.contains('home', na=False)]
df.drop(columns='home', inplace=True)
msk1 = ~df.name_sponsor.str.contains('pniguest', regex=False)
msk2 = ~df.name_sponsor.str.contains('Class account', regex=False)
df = df[msk1 & msk2]
df.drop_duplicates(inplace=True)

# get departments
#print(sorted(df[df.cluster == "other"].name_sponsor.apply(lambda x: x.split(",")[1]).unique()))

# add count (cnt) field
df['cnt'] = df.NETID.apply(lambda x: df[df.NETID == x].shape[0])

# remove adroit entry when second entry exists
msk2 = (df.cnt > 1) & (~df.cluster.str.contains('adroit', regex=False))
df = df[(df.cnt == 1) | msk2]

# assume records are equal in a sense across clusters
df = df[['NETID', 'name_sponsor']].drop_duplicates('NETID', keep='first')

df['NDS'] = df.name_sponsor.apply(extract_name)
df['NAME'] = df.NDS.apply(lambda x: x[0])
df['DEPT']     = df.NDS.apply(lambda x: x[1])
df['SPONSOR']  = df.NDS.apply(lambda x: x[2])
df = df[['NETID', 'NAME', 'DEPT', 'SPONSOR']].sort_values(by='NETID', ascending=True)
df.to_csv('combined_getent.csv', index=False)
