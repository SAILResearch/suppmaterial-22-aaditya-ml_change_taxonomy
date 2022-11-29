#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:10:14 2021
@author: aadityabhatia
info:
    Useful forks term used for changed forks!
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import pandas as pd
from git import Repo

repo_data = pd.read_pickle("Data/whole_ball_of_wax.pkl")
print(repo_data.columns)

# %%
d = []
for index, row in repo_data.iterrows():
    forks = row['forks']
    if len(row['forks']) == 0:
        prop_changed_forks = 0
    else:
        prop_changed_forks = len(row['useful_forks']) / len(row['forks'])
    d.append((row['github_urls'], len(row['forks']), len(row['useful_forks']), prop_changed_forks))

df = pd.DataFrame(d, columns=('github_urls', 'len_forks', 'len_changed_forks', 'prop_useful_forks'))

# removing the noise
df = df[df.len_forks > 0]  # len = 1110

# %% plotting histogram

data = df.prop_changed_forks

fig, ax = plt.subplots()
ax.grid(False)
plt.hist(data, bins=100)
plt.xlabel("Percentage of changed forks")
plt.ylabel("repo count")
plt.show()

# %% plottting CDF

import matplotlib

matplotlib.rcParams.update({'font.size': 12})

fig, ax = plt.subplots()
values, base = np.histogram(data, bins=40)
# evaluate the cumulative
cumulative = np.cumsum(values)

x = 100 * cumulative / len(data)
y = base[:-1] * 100
ax.plot(x, y, c='blue')
ax.set_xlabel('Percentage of Repositories')
ax.set_ylabel('Percentage of Forks_with_changes')

ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
ax.xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()
fig.savefig('plots/cdf_changed_forks.pdf', dpi=3000)

# %%

'''what % of repos do not have any non-trivial fork'''
len(df[df.prop_changed_forks == 0]) / len(df)

k = repo_data[repo_data['prop_non_trivial_forks'] < 0.1]
k = k[["fork_count", "old_changed_count", "non_trivial_fork_count", 'prop_non_trivial_forks', 'prop_useful_forks']]

# %%


''' getting changed fork contributors to mention in the paper '''
contributor_df = pd.read_csv('Data/fork_contributors.csv', sep='\t')
len(contributor_df[contributor_df.fork_contributors <= 0])
contributor_df.fork_contributors.median()
contributor_df.fork_contributors.sum() / len(contributor_df)
