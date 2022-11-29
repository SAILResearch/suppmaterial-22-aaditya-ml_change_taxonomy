#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% IMPORTS

from ast import literal_eval

import numpy as np
import pandas as pd

import ModelDepot_Crawler as scraper

# %% PATH
RELATIVE_PATH = "../data.nosync/"

# %% GIT HUB TENSOFLOW PYTHON URL
DS_TF_PATH = RELATIVE_PATH + "Cloning/data/gitHubTensorFlowURL.csv"

try:
    df_py = pd.read_csv(DS_TF_PATH)
    df_py.drop("Unnamed: 0", axis=1, inplace=True)
except:
    github_urls = scraper.get_results_DS("tensorflow", "tensorflow", "python", "cv")
    github_urls = np.array(github_urls)
    df_py = pd.DataFrame(data=github_urls, columns=["github_urls"])
    df_py.to_csv(DS_TF_PATH)

# %% GIT HUB TENSORFLOW IPYNB URL

DS_IPYNB_PATH = RELATIVE_PATH + "Cloning/data/gitHubIpynbURL.csv"

try:
    df_nb = pd.read_csv(DS_IPYNB_PATH)
    df_nb.drop("Unnamed: 0", axis=1, inplace=True)
except:
    github_urls = scraper.get_results_DS("python", "tensorflow", "jupyter", "cv")
    github_urls = np.array(github_urls)
    df_nb = pd.DataFrame(data=github_urls, columns=["github_urls"])
    df_nb.to_csv(DS_IPYNB_PATH)

# %% UNION OF TWO DATASETS

DS_DIFF_PATH = RELATIVE_PATH + "Cloning/data/gitHubDiffURL.csv"

try:
    df = pd.read_csv(DS_DIFF_PATH)
    df.drop("Unnamed: 0", axis=1, inplace=True)
except:
    df = pd.merge(df_py, df_nb, how='outer')
    df.to_csv(DS_DIFF_PATH)

# %% SAMPLE REPOS TO MANUALLY EXAMINE

print("\nRANDOM SAMPLE FOR MANUAL ANALYSIS\n")

# SAMPLE RANDOM ONES
rnd_smpl = df.sample(n=50, random_state=50)
for path in rnd_smpl['github_urls']:
    link = "https://github.com/" + path
    print(link)

# %% GIT HUB PAPER REFERRENCE
#  KEYWORD -> CONFERENCE-JOURNAL-CITE-NVIDIA-IMPLEMENTATION (so far only "paper")
#  LOOKUP  -> BIBTEX (so far only "arxiv")

# note -> bibtex & implementattion are VERY promising (double results)

ARXIV_PATH = RELATIVE_PATH + "Cloning/data/arxivID.csv"

try:
    df = pd.read_csv(ARXIV_PATH)
    df['arxivIDs'] = df['arxivIDs'].apply(literal_eval)
    df.drop("Unnamed: 0", axis=1, inplace=True)
    df.drop("Unnamed: 0.1", axis=1, inplace=True)
except:
    arxivIDs = scraper.get_arxivIDs(df['github_urls'])
    df['arxivIDs'] = arxivIDs
    df.to_csv(ARXIV_PATH)

# %% Clean Data

number_404 = df[df.arxivIDs == 404].shape[0]
number_df = df.shape[0]
print("\n\nIn the arxivID dataset, there are {}/{} dead links\n\n".format(number_404, number_df))

index_404 = df[df.arxivIDs == 404].index
df.drop(index=index_404, inplace=True)
df.reset_index(inplace=True)

# %% Link IPYNB to repos

ipynb_intersection = pd.merge(df, df_nb, how='inner').github_urls
for index, row in df.iterrows():
    match = (row.github_urls == ipynb_intersection).any()
    if match:
        df.loc[index, 'contains_ipynb'] = True
    else:
        df.loc[index, 'contains_ipynb'] = False

number_NB_paper = np.sum((df.contains_ipynb) & (df.arxivIDs.apply(len) != 0))
number_py_paper = np.sum((df.contains_ipynb == False) & (df.arxivIDs.apply(len) != 0))
number_nb = df_nb.shape[0]
number_py = df_py.shape[0]
print("\n\nNumber NB with paper {}/{}".format(number_NB_paper, number_nb))
print("Number NB with paper {}/{}\n\n".format(number_py_paper, number_py))

# %% LINK PAPER TO REPO

# OUTPUTS    df_linked
#   columns:    paper_id     (arxiv ID)
#               github_urls  (related to id)
#               number_repos (# of github_urls)

df_linked = pd.DataFrame()
df_linked['paper_id'] = []
df_linked['github_urls'] = []
df_linked['number_repos'] = []

for index, row in df.iterrows():
    for paper in row['arxivIDs']:
        linked = False
        linked_list = []

        id_not_added = (paper != df_linked['paper_id']).all()
        if id_not_added:

            for i in range(index + 1, df.shape[0]):

                list_of_remaining_ids = df.loc[i, 'arxivIDs']
                if paper in list_of_remaining_ids:
                    linked = True
                    linked_list.append(df.loc[i, 'github_urls'])
                    print("LINK {} - {} : ID {}".format(index, i, paper))

            linked_list.insert(0, df.loc[index, 'github_urls'])
            df_linked = df_linked.append({'paper_id': paper, 'github_urls': linked_list}, ignore_index=True)

df_linked['number_repos'] = df_linked['github_urls'].apply(len)
LINK_PATH = RELATIVE_PATH + "Cloning/data/arxiv_linked.csv"
df_linked.to_csv(LINK_PATH)

# %% MANUALLY RANDOM SAMPLE REPOS TO EXAMINE
rnd_smpl = df_linked.sample(n=50, random_state=50)
rnd_smpl.to_csv('../temp/inspect_repos.csv', index=0)
