#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 11 21:59:46 2021
@author: aadityabhatia

info:
    number of days elapsed before forks created/PR submitted/PR merged (actual & cumulative)
    for each repo, compare creation time with creation time of each of its forks

"""

import matplotlib.pyplot as plt
import pandas as pd


'''AFTER FORKING, it takes ? days for forked repo to give a PR to parent repo?'''

df = pd.read_csv("Data/summary_repo_pr.csv", sep='\t')

forked = df[df.is_fork]
len(forked)
len(forked[forked.is_merged])
'''this is 607 = "paper txt: A total of 607 pull requests were submitted upstream out of these only 316 were merged '''

# %%

forked = forked[~forked.pr_from_date.isna()]
forked = forked[~forked.pr_date.isna()]

forked['pr_from_date'] = pd.to_datetime(forked['pr_from_date'].astype(str))
forked['pr_date'] = pd.to_datetime(forked['pr_date'].astype(str))

print(len(forked[forked.pr_date == forked.pr_from_date]))  # should be 0

forked['timegap_hours'] = (forked.pr_date - forked.pr_from_date).dt.total_seconds() / (3600)
forked['timegap_day'] = (forked.pr_date - forked.pr_from_date).dt.total_seconds() / (60 * 60 * 24)  # days
forked['timegap_days'] = (forked.pr_date - forked.pr_from_date).dt.days

# %%
# getting pr_date and merege_date
merged = forked[forked.is_merged]

print(len(merged[merged.merged_date.isna()]))  # o nice
try:
    merged['merged_date'] = pd.to_datetime(merged['merged_date'])
except:
    print('already pd date format')
merged['merge_time'] = (merged.merged_date - merged.pr_date).dt.total_seconds() / (3600)  # 60*60

# %%
import matplotlib

matplotlib.rcParams.update({'font.size': 12})
fig, ax = plt.subplots()
violin_parts = ax.violinplot([forked.timegap_hours, merged.merge_time], [1, 2])

for partname in ('cbars', 'cmins', 'cmaxes'):
    vp = violin_parts[partname]
    vp.set_edgecolor('black')
    vp.set_linewidth(1)

ax.set_xticks([1, 2])
ax.set_xticklabels(['PR Creation\nTime', "PR Merging\nTime"])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ax.set_ylabel('Hours')
fig.tight_layout()
fig.show()
fig.savefig('plots/Forking_merging_times.pdf', dpi=3000)

# %% stuff to report in paper!
print(forked.timegap_hours.median())
print(merged.merge_time.median())
#%%