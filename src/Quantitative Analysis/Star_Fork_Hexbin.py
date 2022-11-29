#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 18:45:58 2021
@author: aadityabhatia
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DIR = 'Data/'

df = pd.read_csv(DIR + "github_repos_stats.csv", sep='\t')

# %%
""" PREPARING DATA"""

for col in df.columns:
    try:
        print(df["{}".format(col)].median(), col)
    except:
        pass

forks = pd.read_csv(DIR + 'summary_repo_forks.csv', sep='\t')
print(len(forks))  # this is good! 1338
len(forks[forks.forks == 0])

df = pd.merge(df, forks, on='github_urls', how='right')

'''logging the star count '''
df['stars_log'] = np.log10(df['stars'] + 1)
df['forks_log'] = np.log10(df['forks'] + 1)
df = df.dropna()

df.head()

# %%
'''getting CORRELATION'''

from scipy.stats import pearsonr, spearmanr

# checking the pearson corr
corr, _ = pearsonr(df.forks, df.stars)
print(corr, 'normal')

corr, _ = pearsonr(df.forks_log, df.stars_log)
print(corr, 'logged')

# Spearmann corr

corr, _ = spearmanr(df.forks, df.stars)
print(corr, 'normal')

corr, _ = spearmanr(df.forks_log, df.stars_log)
print(corr, 'logged')

# %% getting median counts

print(df.stars.median())
print(df.forks.median())

# %%  testing with df where forks are not there

df_isFork = df[df.forks > 0]
x, y = df_isFork.forks_log, df_isFork.stars_log

xmin = x.min()
xmax = x.max()
ymin = y.min()
ymax = y.max()

# %% plotting the repos vs forks correlations as hexbins

import matplotlib

matplotlib.rcParams.update({'font.size': 12})

fig, ax = plt.subplots()
hb = ax.hexbin(x, y, gridsize=15, cmap='binary')  # inferno, cividis
ax.axis([xmin, xmax, ymin, ymax])
cb = fig.colorbar(hb, ax=ax)
cb.set_label('Repository Count')

ax.set_xlabel('# Forks (Log Base 10) ')
ax.set_ylabel('# Stars (Log Base 10) ')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.show()
fig.savefig( 'plots/repo_stars_forks.pdf', dpi = 3000)


# %%


"""
COMPARISON WITH BRISSON'S RESEARCH
"""

comm = pd.read_csv('Data/Brissons-package/comm_metrics.csv')

print('forks',
      comm.forks.median(), 'median \count', \
      comm.forks.mean(), \
      )
corr, _ = spearmanr(comm.forks, comm.stars)
print(corr)

'''Mann whitney U test '''

from scipy.stats import ranksums

print(ranksums(df.forks, comm.forks))
print(ranksums(df.stars, comm.stars))
