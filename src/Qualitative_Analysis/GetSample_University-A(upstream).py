#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% IMPORTS

import math
import random

import numpy as np
import pandas as pd

# %% PATHS & CONSTANTS

DATA_PATH = '../data.nosync/'

# GET DATA
df = pd.read_pickle(DATA_PATH + 'final_sample.pkl')

PEOPLE = 3

# %%
for c in df.columns:
    print(type(df[c].iloc[0]), c)

""" Aadi:  
    We had a df of 23 github urls (the top 5%)
    Now we get a stratified sample wrt the forks, 
    ie, some Repos have high fork_mods some have low, 
    each fork mod has PRs.
    
    Hence, wrt ratio of fork mods per repo, we get
    stratified sample of PRs. 
"""

# %% DIVIDE FORKS
"""
GET TOPN BY CRITERIAS (us_fork / us_by / pr_merged)
n_forks = df.useful_forks.apply(len)
n_pullreq = df.merged_pull_req.apply(len)
frk_95p = np.percentile(n_forks, 95)
pr_95p = np.percentile(n_pullreq, 95)
sample = df[(n_forks > frk_95p) & (n_pullreq > pr_95p)]
"""
sample = df

# 445 PR -> 207
n_PR = np.sum(sample.merged_pull_req.apply(len))
# 1648 FORKS -> 312
n_FORKS = np.sum(sample.useful_forks.apply(len))

if n_PR != 445 or n_FORKS != 1648:
    raise Exception("Redo 95-5 calculation!")

n_PR_strat = 207
n_FORKS_strat = 312

# df.to_pickle(DATA_PATH + 'final_sample.pkl')

# %% STRAT SAMPLE

# proportionnate strat. sampl.
percentage_PR = []
for n in sample.merged_pull_req.apply(len):
    percentage_PR.append(n / n_PR)

percentage_FORKS = []
for n in sample.useful_forks.apply(len):
    percentage_FORKS.append(n / n_FORKS)

pr_sample = []
for pull_reqs, i in zip(sample.merged_pull_req, range(len(sample.merged_pull_req))):
    sample_size = int(math.ceil(percentage_PR[i] * n_PR_strat))
    smpl = random.sample(pull_reqs, sample_size)
    smpl_url = [x['_links']['html']['href'] for x in smpl]
    pr_sample += smpl_url

frk_sample = []
for forks, i in zip(sample.useful_forks, range(len(sample.useful_forks))):
    sample_size = int(math.ceil(percentage_FORKS[i] * n_FORKS_strat))
    smpl = random.sample(forks, sample_size)
    frk_sample += smpl

# %% DIVISION

random.shuffle(pr_sample)
sample = pr_sample

tuples = []
for i in range(PEOPLE):
    for j in range(i + 1, PEOPLE):
        tuples.append((i, j))

division = len(tuples)
sample_sizes = math.floor(len(sample) / division)
remainder = len(sample) % division

samples = []
for i in range(division):
    low_bound = i * sample_sizes
    up_bound = (i + 1) * sample_sizes
    samples.append(sample[low_bound:up_bound])
for i in range(remainder):
    samples[i].append(sample[-i])

people_samples = []
for i in range(PEOPLE):
    people_samples.append([])

for i in range(division):
    first = tuples[i][0]
    second = tuples[i][1]
    sample = samples[i]

    people_samples[first] += (sample)
    people_samples[second] += (sample)


# %% FIND i,j index

def get_df_fork_index(df, fork_name):
    for i, row in df.iterrows():
        for j in range(row.number_useful_forks):
            if row.useful_forks[j] == fork_name:
                return (i, j)
    raise Exception("index not found")


def get_df_pullReq_index(df, pullReq_url):
    for i, row in df.iterrows():
        for j in range(len(row.pull_req)):
            if row.pull_req[j]['html_url'] == pullReq_url:
                return (i, j)
    raise Exception("index not found")


def get_pullReq_commits(df, pullReq_url):
    index = get_df_pullReq_index(df, pullReq_url)
    pullReq_commits = df.loc[index[0], 'pull_req_commits'][index[1]]
    return pullReq_commits


# %% PUT IN CSV FORM

IMPLEMENTATION = ["feature", "platform"]
MAINTENANCE = ["bug fix", "debug", "cross", "preprocessing", "model change", "training change", "accuracy",
               "performance", "security", "maintenance"]
MODULE_MANAGEMENT = ["add module", "move module", "remove module", "split module"]
DEPENDENCY_MANAGEMENT = ["add package", "remove package", "update package"]
LEGAL = ["liscence"]
NON_FCT_SC_CHNG = ["clean up", "token replace", "refactor", "indent"]
SCS_MNGMNT = ["branch", "external", "merge", "versioning", "source control"]
META_PROG = ["build/config", "testing", "documentation", "internationalization"]
DATA = ["input data", "output data", "program data", "exploit additional data"]
MISC = ["understanding", "param tinkering", "sharing"]

CATEGORIES = IMPLEMENTATION + MAINTENANCE + MODULE_MANAGEMENT + DEPENDENCY_MANAGEMENT + LEGAL + NON_FCT_SC_CHNG + SCS_MNGMNT + META_PROG + DATA + MISC

i = 0
for individual_sample in people_samples:

    indices = []
    for pr in individual_sample:
        index = get_df_pullReq_index(df, pr)
        indices.append(index)

    sorted_sample = [x for _, x in sorted(zip(indices, individual_sample), key=lambda pair: pair[0])]

    indices.sort(key=lambda tup: tup[0])

    df_smpl = pd.DataFrame([])
    df_smpl['sample_url'] = ''
    df_smpl['commit_url'] = ''
    df_smpl['notes'] = ''
    for category in CATEGORIES:
        df_smpl[category] = ''

    for pull_req in sorted_sample:
        current_row = len(df_smpl)
        df_smpl.loc[current_row, 'sample_url'] = pull_req

        commits = get_pullReq_commits(df, pull_req)
        for commit in commits:
            current_row = len(df_smpl)
            df_smpl.loc[current_row, 'commit_url'] = commit['html_url']

    df_smpl.to_csv(DATA_PATH + 'Data_For_Universities/' + 'upstream_sample_{}.csv'.format(i), index=False)
    i += 1
