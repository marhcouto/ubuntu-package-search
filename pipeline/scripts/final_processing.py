#!/usr/bin/env python3

import pandas as pd
import re

df = pd.read_csv('out/csv_data/clean/all.csv', dtype={'Essential': str})
df['Depends'] = df['Depends'].fillna("")
df['Recommends'] = df['Recommends'].fillna("")
df['Suggests'] = df['Suggests'].fillna("")
df['Breaks'] = df['Breaks'].fillna("")
df['Conflicts'] = df['Conflicts'].fillna("")
df['Replaces'] = df['Replaces'].fillna("")

def filter_fn(x):
    if(isinstance(x, str)):
        clean_sec = str(x).split('/')
        if(len(clean_sec) == 2):
            return clean_sec[1]
        else:
            return x

# These columns only had null values
df = df.drop(columns=['Installed-Size', 'Pre-Depends'])
df['Section'] = df['Section'].apply(filter_fn)
df['Essential'] = df['Essential'].fillna(value='no')

def remove_version(x):
    striped_x = x.strip()
    return striped_x.split(' ')[0]

def transform_list(string_list):
    no_spec_char_str = "".join([x for x in string_list if x not in ['[', ']', "'"]])
    list_items = no_spec_char_str.split(',')
    no_version_items = [remove_version(x) for x in list_items]
    return " ".join(no_version_items)

df['Depends'] = df['Depends'].apply(transform_list)
df['Recommends'] = df['Recommends'].apply(transform_list)
df['Suggests'] = df['Suggests'].apply(transform_list)
df['Breaks'] = df['Breaks'].apply(transform_list)
df['Conflicts'] = df['Conflicts'].apply(transform_list)
df['Replaces'] = df['Replaces'].apply(transform_list)

df.to_csv('out/csv_data/clean/final.csv', index=False)

df['Description'] = df['Description'].apply(lambda x: x.replace("\\n", " "))
df = df.drop(columns=['Version'])

df.to_csv('out/csv_data/clean/final_solr.csv', index=False)
