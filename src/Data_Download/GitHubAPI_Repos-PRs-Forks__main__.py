#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
We perform incremental addition of features into the data file (dict.pkl),
Since these processes are highly time intensive!
We use spyder/pycharm IDE cell functionality to process in a Jupyter-like fashion.
'''
# %% IMPORT

import pandas as pd
import GitHubAPI_methods as forks

# %% PATHS & CONSTANTS


DATA_PATH = '../Data.nosync/final_sample_w_dict.pkl'

# %% GET DATA
df = pd.read_pickle(DATA_PATH)

# %% MINE UPSTREAM COMMITS URLS FROM GITHUB
user = input('username : ')
passwd = input('password : ')

i = 0
useful_upstream_commits_dict = []
for index, repo in df.iterrows():
    print("{}/{}".format(i, df.shape[0]))
    upstream_commits = forks.get_commits(repo.github_urls, user, passwd)
    useful_upstream_commits_dict.append(upstream_commits)
    i += 1

df['useful_upstream_commits_dict'] = useful_upstream_commits_dict

df.to_pickle(DATA_PATH + 'final_sample_w_dict.pkl')

# %% MINE FORKS COMMITS URLS FROM GITHUB

user = input('username : ')
passwd = input('passwd :   ')

i = 0
useful_forks_commits_dict = []
for index, repo in df.iterrows():
    j = 0
    ufcd = []
    for fork_url in repo.useful_forks:
        print("{}/{}".format(i, df.shape[0]))
        print("{}/{}".format(j, len(repo.useful_forks)))
        fork_commits = forks.get_commits(fork_url, user, passwd)
        ufcd.append(fork_commits)
        j += 1
    useful_forks_commits_dict.append(ufcd)
    i += 1

df['useful_forks_commits_dict'] = useful_forks_commits_dict
df.to_pickle(DATA_PATH + 'final_sample_w_dict.pkl')

# %% ASSOCIATE USEFUL AND USELESS

ufc = []
for index, repo in df.iterrows():
    upstream_commits = [commit['commit']['author'] for commit in repo.useful_upstream_commits_dict]
    unique_forks_commits = []
    for fork_commits in repo.useful_forks_commits_dict:
        unique_fork_commits = [commit for commit in fork_commits if commit['commit']['author'] not in upstream_commits]
        unique_forks_commits.append(unique_fork_commits)
    ufc.append(unique_forks_commits)

df['unique_forks_commits_dict'] = ufc
df.to_pickle(DATA_PATH + 'final_sample_w_dict.pkl')

# %% GET THE STATS OF THE COMMITS
user = input('username : ')
passwd = input('passwd :   ')

i = 0
unique_commits_dict = []
for index, repo in df.iterrows():
    j = 0
    repo_ucd = []
    for fork in repo.unique_forks_commits_dict:
        k = 0
        fork_ucd = []
        for commit in fork:
            print("{}/{} UPSTREAM".format(i, df.shape[0]))
            print("{}/{} FORKS".format(j, len(repo.unique_forks_commits_dict)))
            print("{}/{} COMMITS\n\n\n\n\n\n\n\n".format(k, len(fork)))
            commit_url = commit['url']
            commit_dict = forks.get_requests(commit_url, user, passwd)
            fork_ucd.append(commit_dict)
            k += 1
        repo_ucd.append(fork_ucd)
        j += 1
    unique_commits_dict.append(repo_ucd)
    i += 1

df['unique_commits_dict'] = unique_commits_dict
df.to_pickle(DATA_PATH + 'final_sample_w_dict.pkl')

# %% FILTER 0 COMMITS CAUSE FORGOT BEFORE!

unique_commits_dict = []
for index, repo in df.iterrows():
    fork_commits = [commits for commits in repo.unique_commits_dict if len(commits) != 0]
    unique_commits_dict.append(fork_commits)

df['unique_commits_dict'] = unique_commits_dict
df.to_pickle(DATA_PATH + 'final_sample_w_dict.pkl')
