#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 12:13:32 2021
@author: aadityabhatia
"""

import pandas as pd
from nltk.metrics import masi_distance
from nltk.metrics.agreement import AnnotationTask

dir_ = 'src/Qualitative_Analysis/'
# %% Getting alpha values from different IR csvs.

def getKreppendoffAlpha(downstream_df):
    downstream_df = downstream_df.fillna("")

    # columns are in the first row
    colnames = list(downstream_df.iloc[0])
    downstream_df = downstream_df.drop(0, axis=0)
    downstream_df.columns = colnames

    sample_url = downstream_df['sample_url']
    downstream_df = downstream_df.drop('sample_url', axis=1)

    new_data = pd.DataFrame()
    for i, row in downstream_df.iterrows():  # iterate rows
        rater_names = set()
        for c in downstream_df.columns:
            rater_names.update(row[c])

        """ this is bad sample"""
        if len(rater_names) < 2:
            print('heres where the issue lies', i)
            # continue

        df = pd.DataFrame(row)
        df.columns = ['rater']
        for i, rater in enumerate(rater_names):
            df['rater'] = df.rater.str.replace(rater, 'Rater_{}'.format(i))

        df = df.transpose()

        new_data = new_data.append(df)

    new_data = new_data.reset_index(drop=True)

    task_data = []
    for i, row in new_data.iterrows():
        lst_0 = []
        lst_1 = []
        lst_2 = []

        for c in new_data.columns:
            if '0' in row[c]:
                lst_0.append(c)
            if '1' in row[c]:
                lst_1.append(c)
            if '2' in row[c]:
                lst_2.append(c)

        if len(lst_0):
            task_data.append(('Rater0', str(i), frozenset(lst_0)))
        if len(lst_1):
            task_data.append(('Rater1', str(i), frozenset(lst_1)))
        if len(lst_2):
            task_data.append(('Rater2', str(i), frozenset(lst_2)))

    task = AnnotationTask(distance=masi_distance)
    task.load_array(task_data)
    print(task.alpha(), "KREPPENDOFF!")

    # getting the data in format Rater 1, Rater 2 rated what..
    # format is compatible with the plotting script
    return new_data


if __name__ == '__main__':
    down_1st = pd.read_csv(dir_ + 'down_round1.csv')
    down_2nd = pd.read_csv(dir_ + 'down_round2.csv')
    down_final = pd.read_csv(dir_ + 'down_final.csv')

    # first and second rounds without resolution of discrepancies.
    _ = getKreppendoffAlpha(down_1st)
    _ = getKreppendoffAlpha(down_2nd)

    # final resolution of discrepancies
    df = getKreppendoffAlpha(down_final)
    df.to_csv(dir_ + '../downstream_processed.csv')
