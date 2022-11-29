# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Aaditya Bhatia
This script obtains stats for reporting!
"""

import pandas as pd

dir_ = '../data.nosync/'

'''this is the repos dataset with creation date'''
sampled_repos = pd.read_csv(dir_ + "summary_repo_pr.csv", sep='\t')
useful_forks = pd.read_pickle(dir_ + 'github_repos_list.pkl')

# %% how many forks per repo!

useful_forks['fork_count'] = useful_forks['forks'].apply(len)
u = useful_forks[['github_urls', 'fork_count']]


# %%

def get5numSummary(data):
    from numpy import percentile
    quartiles = percentile(data, [25, 50, 75])
    # calculate min/max
    data_min, data_max = data.min(), data.max()
    # print 5-number summary
    print('Min: %.3f' % data_min)
    print('Q1: %.3f' % quartiles[0])
    print('Median: %.3f' % quartiles[1])
    print('Q3: %.3f' % quartiles[2])
    print('Max: %.3f' % data_max)


get5numSummary(u.fork_count.to_numpy())

len(u[u.fork_count == 0])

'''
so we report 1346 in forks in the paper
'''

# %%

cols = ['arxivIDs', 'forks', 'useful_forks', 'commits', 'merge_commits', 'forks_commits', 'pull_req',
        'merged_pull_req', 'unmerged_pull_req', 'pull_req_commits']

vis_df = pd.DataFrame()
vis_df['repo_url'] = useful_forks['github_urls']
for c in cols:
    vis_df[c + '_count'] = useful_forks[c].apply(lambda x: len(x))

# %%

""" getting the stats """
print("total forks in all repos:", vis_df['forks_count'].sum())
print("total useful forks in all repos:", vis_df['useful_forks_count'].sum())
print("total pull requests in all repos:", vis_df['pull_req_count'].sum())
