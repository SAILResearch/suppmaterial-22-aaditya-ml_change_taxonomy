#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% IMPORT

import math
import random
import numpy as np
import pandas as pd

# %% PATHS & CONSTANTS

DATA_PATH = '../data.nosync/'

# GET DATA
df = pd.read_pickle(DATA_PATH + 'final_sample_w_dict.pkl')

PEOPLE = 3

# %%

sample = df.copy()

def get_pylines_added_fork(f):
    loc = 0
    for commit in f:
        loc += get_pylines_added_dict(commit)
    return loc


def get_pylines_added_dict(d):
    loc = 0
    for file in d['files']:
        extension = file['filename'].split('.')[-1]
        if extension == 'py':
            loc += file['additions']
    return loc


n_loc = []
for index, repo in sample.iterrows():
    repo_loc = []
    for fork_commits in repo.unique_commits_dict:
        loc = np.sum([get_pylines_added_dict(commit) for commit in fork_commits])
        repo_loc.append(loc)
    n_loc.append(repo_loc)
sample['n_loc_per_fork'] = n_loc

# %% DIVIDE FORKS

n_FORKS_COMMITS = 0
ncpf = []
for forks in sample.unique_commits_dict_below_5000:
    n_commits_per_fork = []
    for fork in forks:
        for commit in fork:
            n_FORKS_COMMITS += 1
        n_commits_per_fork.append(len(fork))
    ncpf.append(n_commits_per_fork)
sample['n_commits_per_fork'] = ncpf

if n_FORKS_COMMITS != 10817:
    raise Exception("Redo 95-5 calculation!")

n_FORKS_COMMITS_strat = 372

# %% RANDOM PROPORTIONATE STRATIFICATION

# proportionate strat. sampl. by n_forks
percentage_COMMITS = []
for n in sample.unique_commits_dict_below_5000.apply(len):
    percentage_COMMITS.append(n / np.sum(sample.unique_commits_dict_below_5000.apply(len)))

commit_sample = []
for fork, percentage in zip(sample.unique_commits_dict_below_5000, percentage_COMMITS):
    sample_size = int(math.ceil(percentage * n_FORKS_COMMITS_strat))
    fork_commits = [commit for commits in fork for commit in commits]
    smpl = random.sample(fork_commits, sample_size)
    smpl_url = [item['url'] for item in smpl]
    commit_sample += smpl_url

# %% DIVISION

random.shuffle(commit_sample)
sample = commit_sample

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


# %% FIND i,j,k index

def get_url_commit_index(url):
    for i, row in df.iterrows():
        for j in range(len(row.unique_commits_dict_below_5000)):
            for k in range(len(row.unique_commits_dict_below_5000[j])):
                if row.unique_commits_dict_below_5000[j][k]['url'] == url:
                    return (i, j, k)
    raise Exception("index not found")


# %% PUT IN CSV FORM

IMPLEMENTATION = ["feature", "platform"]
MAINTENANCE = ["bug fix", "debug", "cross", "preprocessing", "model change", "training change", "accuracy", "performance",
                "security", "maintenance"]
MODULE_MANAGEMENT = ["add module", "move module", "remove module", "split module"]
DEPENDENCY_MANAGEMENT = ["add package", "remove package", "update package"]
LEGAL = ["license"]
NON_FCT_SC_CHNG = ["clean up", "token replace", "refactor", "indent"]
SCS_MNGMNT = ["branch", "external", "merge", "versioning", "source control"]
META_PROG = ["build/config", "testing", "documentation", "internationalization"]
DATA = ["input data", "output data", "program data", "exploit additional data"]
MISC = ["understanding", "param tinkering", "sharing"]

CATEGORIES = IMPLEMENTATION + MAINTENANCE + MODULE_MANAGEMENT + DEPENDENCY_MANAGEMENT + LEGAL + NON_FCT_SC_CHNG + SCS_MNGMNT + META_PROG + DATA + MISC

i = 0
for individual_sample in people_samples:

    indices = []
    for commit in individual_sample:
        index = get_url_commit_index(commit)
        indices.append(index)

    sorted_sample = [x for _, x in sorted(zip(indices, individual_sample), key=lambda pair: pair[0])]

    indices.sort(key=lambda tup: tup[0])

    df_smpl = pd.DataFrame([])
    df_smpl['commit_url'] = ''
    df_smpl['notes'] = ''
    for category in CATEGORIES:
        df_smpl[category] = ''

    for commit in sorted_sample:
        current_row = len(df_smpl)
        df_smpl.loc[current_row, 'commit_url'] = commit

    df_smpl.to_csv(DATA_PATH + 'Data_For_Universities/' + 'downstream_sample_{}.csv'.format(i), index=False)
    i += 1
