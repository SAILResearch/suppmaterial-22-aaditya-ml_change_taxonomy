#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 22:00:22 2021

@author: aadityabhatia
"""

import pandas as pd

RELATIVE_PATH = "../data.nosync/"
PATH = RELATIVE_PATH + "github_repos_list.pkl"

df = pd.read_pickle(PATH)

cols = ['github_urls', 'arxivIDs', 'forks', 'useful_forks', 'source_path',
        'forks_paths', 'commits', 'merge_commits', 'forks_commits', 'pull_req',
        'merged_pull_req', 'unmerged_pull_req', 'pull_req_commits',
        'dependents', 'dependencies', 'dependents_forks', 'dependencies_forks']

def getName(frk):
    ret = []
    for f in frk:
        ret.append(f['full_name'])
    return ret

# %%  getting additional features

df['count_useful_forks'] = df.useful_forks.apply(len)
df['count_forks'] = df.forks.apply(len)
df['frk_name'] = df.forks.apply(getName)

#%% inspecting an element!
num = 8
print(df.iloc[num].github_urls)
print(df['count_useful_forks'].iloc[num])
print(df['count_forks'].iloc[num])
print(df['frk_name'].iloc[num])

# %%
