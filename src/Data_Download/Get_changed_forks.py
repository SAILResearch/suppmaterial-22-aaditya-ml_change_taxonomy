#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 18:49:09 2021

@author: aadityabhatia

useful forks converted into non trivial forks.
non trivial are the so called "forks_with_changes" in the paper.
"""

import pandas as pd
pkl_path = 'data/whole_ball_of_wax.pkl'

# %%

def getPR_clone_url(pr_lst):
    who_sent_pr = []
    # for each pr of the repo
    for pr_dct in pr_lst:
        try:
            pr = pr_dct['head']['repo']['full_name']
            who_sent_pr.append(pr)
        except:
            print('None pr submitter')

    return who_sent_pr

df = pd.read_pickle('Data/github_repos_list.pkl')
df['aadi_pr_submitters'] = df.pull_req.apply(getPR_clone_url)

# %%

william_missed = []

total_missed = []
for i, row in df.iterrows():
    useful_forks = row.useful_forks.copy()  # copy is imp or else it changes the actual df itself!
    useful_forks.append(row.github_urls)  # because the actual repo holder also forks

    miss = []
    for p in row.aadi_pr_submitters:
        p = p.lower()  # sometimes repo_name is in upper, even tho its in useful_list we still add it
        if p not in useful_forks:
            miss.append(p)
            total_missed.append(p)
    william_missed.append(list(set(miss)))

df['useful_forks_in_prs'] = william_missed

# %%
df['non_trivial_forks'] = df.useful_forks + df.useful_forks_in_prs

# %%
print(len(set(total_missed)))


def getLen(st):
    return len(set(st))


df['fork_count'] = df['forks'].apply(len)
df['old_useful_count'] = df['useful_forks'].apply(getLen)
df['actual_useful_count'] = df.non_trivial_forks.apply(getLen)

# %%  overall percentage of non_trivial forks

''' old william analysis was missed check '''
100 * df.old_useful_count.sum() / df['fork_count'].sum()

'''new actual counts '''
100 * df.actual_useful_count.sum() / df['fork_count'].sum()

# %%
''' how many repos had 0 forks? '''

df1 = df[df.fork_count > 0]
len(df) - len(df1)

''' old william analysis was wrong '''
100 * df1.old_useful_count.sum() / df1['fork_count'].sum()
100 * df.old_useful_count.sum() / df['fork_count'].sum()

'''new actual counts '''
100 * df1.actual_useful_count.sum() / df1['fork_count'].sum()
100 * df.actual_useful_count.sum() / df['fork_count'].sum()

# %%  per fork percentage

df['percentage_non_trivial'] = 100 * df.actual_useful_count / df['fork_count']
print(df['percentage_non_trivial'].median(), df['percentage_non_trivial'].mean())

# %%

df['PR_submitters'] = df.pull_req.apply(getPR_clone_url)
df[['github_urls', 'arxivIDs', 'forks', 'useful_forks', 'source_path',
    'commits', 'merge_commits', 'forks_commits', 'pull_req',
    'merged_pull_req', 'unmerged_pull_req', 'pull_req_commits',
    'dependents', 'dependencies', 'dependents_forks', 'dependencies_forks',
    'useful_forks_in_prs', 'non_trivial_forks', 'PR_submitters']].to_pickle(pkl_path)

# %%
""" getting stats for:
        What % of PR submitters were from useful forks??
"""

# first preprocesing to get actual count by removing the repo holders!
df['tmp_pr_sub_count'] = df.PR_submitters.apply(len)
# removing the original developer from PR submitters list:

for i, row in df.iterrows():
    if row.github_urls in row['PR_submitters']:
        row['PR_submitters'].remove(row.github_urls)

df['tmp_new_pr_sub_count'] = df.PR_submitters.apply(len)

print(
    df['tmp_new_pr_sub_count'].mean()
    , df['tmp_pr_sub_count'].mean()
)  # means algo worked

df['non_trivial_fork_count'] = df.non_trivial_forks.apply(len)

# NOW GETTING THE FINAL COUNT
print(df.tmp_new_pr_sub_count.sum() / df.non_trivial_fork_count.sum())
