#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 11:10:14 2021
@author: aadityabhatia
"""

import pandas as pd
DATA_PATH = 'Data/'

# %% Getting transitive forking stats!

trans = pd.read_csv(DATA_PATH + 'transitive_forks_stats.csv', sep='\t')

# each git url has multiple forks, so we need to aggregate!
trans = trans.fillna(0)
trans_grp = trans.groupby('github_urls', as_index=0).agg({'forks': 'count', 'level_1': 'sum',
                                                          'level_2': 'sum', 'level_3': 'sum',
                                                          'level_4': 'sum'})
# here's the transitive data !
trans_grp.forks.median()

# checking how many repos have forks
l1 = trans_grp[trans_grp.level_1 > 0].level_1.sum()
l2 = trans_grp[trans_grp.level_2 > 0].level_2.sum()
l3 = trans_grp[trans_grp.level_3 > 0]
l4 = trans_grp[trans_grp.level_4 > 0]  # these are none

# %%
''' All my trans stats to report in the paper '''

df = pd.read_csv(DATA_PATH + 'summary_repo_forks.csv', sep='\t')
df.forks.median()
for col in trans_grp.columns:
    try:
        print(col, "STATS::")
        print(col, trans_grp['{}'.format(col)].median(), 'median')
        print(col, trans_grp['{}'.format(col)].mean(), 'mean')
        print(col, trans_grp['{}'.format(col)].max(), 'max')
        print(col, trans_grp['{}'.format(col)].sum(), 'sum or total')
        print(len(trans_grp[trans_grp['{}'.format(col)] > 0]), 'total repos with', col, 'trans')
        print()
    except:
        pass
'''
# %%  comparing against Brissons data!

a1 = pd.read_csv('Data/Brissons-package/comm_metrics.csv')

# %of repos having active forks
print(len(a1[a1.active_forks > 0]) / len(a1))

# % of forks being active forks
print(a1.active_forks.sum() / a1.forks.sum())

# %%  USING R WITHIN PYTHON!
% load_ext
rpy2.ipython

# %% MAGIC CELL MAGIC!!
%%R

library(graphics)

brissons_data = c(385, 12171, 778, 84, 11, 2)
our_data = c(1581, 44, 7, 0, 0, 0)

chisq_df < - data.frame(brissons_data, our_data)
mosaicplot(chisq_df, shade=TRUE, las=2,
           main="housetasks")
print(chisq_df)
chisq < - chisq.test(chisq_df)
print(chisq)

# %%
'''