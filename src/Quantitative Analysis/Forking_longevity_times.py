import pandas as pd
from matplotlib import pyplot as plt

# %%

dir_ = 'Data/'

'''this is the repos dataset with creation date'''
sampled_repos = pd.read_csv(dir_ + "summary_repo_pr.csv", sep='\t')
repos_dates = sampled_repos.loc[:, 'github_urls':'creation_date'].drop_duplicates(subset=None, keep='first',
                                                                                  inplace=False).copy()


# %%
""" Getting first dreation """

df = pd.read_csv(dir_ + "summary_forks_date.csv", sep='\t')
df = df[df['github_urls'].isin(repos_dates['github_urls'])].copy()
df['fork_creation_date'] = pd.to_datetime(df['fork_creation_date'])
df['min_date'] = df['fork_creation_date']
df['max_date'] = df['fork_creation_date']

gp = df[['min_date', 'max_date', 'github_urls']].groupby('github_urls', as_index=0).agg({
    'min_date': 'min', 'max_date': 'max'
})

# %%
repos_dates['repo_time'] = pd.to_datetime(repos_dates.creation_date)

times = pd.merge(gp, repos_dates, on='github_urls')

times['min_time'] = (times['min_date'] - times.repo_time).dt.days
times['max_time'] = (times['max_date'] - times.repo_time).dt.days

times = times.dropna()


# %%
import matplotlib
matplotlib.rcParams.update({'font.size': 12})

fig, ax = plt.subplots()
ax.boxplot([times.min_time, times.max_time])
ax.set_xticklabels(['First Fork', 'Final Fork'])
ax.set_ylabel('Time in Days')

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

fig.tight_layout()
fig.show()
# fig.savefig('plots/forking_min_max_times.pdf', dpi=3000)

print(times.min_time.median(), times.max_time.median())
