'''
@info:
    1.
    all the ones with single rating are discarded!
    multi ones are the ones we get

    2.
    all with (d) are to be removed, they are disagreement sample

    3.
    all the ones with '2' are basically 'AB' as they were made later, the authors later agree on them.



basically, wherever there is "resolved" in the second resolve, thats where the round 2 had issues.
basically wherever "partially/disagree" in round 1 thats where we had issues in Round 1.
'''

import pandas as pd
from nltk.metrics import masi_distance
from nltk.metrics.agreement import AnnotationTask

dir = 'src/Qualitative/googleSheets/'

do = pd.read_csv(dir + 'downstream_york.csv')

"""# filtering columns"""
do = do.fillna("")

colnames = list(do.iloc[0])
colnames[0] = 'PR_url'
colnames[1] = 'Commit_url'
colnames[2] = '1stResolve'
colnames[3] = '2ndResolve'

do = do.drop(0, axis=0)
do.columns = colnames

del do['notes']

# PR_url      = do['PR_url']
# Commit_url  = do['Commit_url']
# res1        = do['1stResolve']
# res2        = do['2ndResolve']
# del do['PR_url'], do['Commit_url'], do['1stResolve'], do['2ndResolve']

# %%
'''
Doin the 1st resolve now
Heuristic:
    - remove (a) or (d)
    - remove 2
    - remove whitespaces
    - Lets make A coder same as D    
'''


def cleanFor1Res(x):
    x = x.replace("(a)", "")
    x = x.replace("(d)", "")
    x = x.replace(" ", "")
    x = x.replace("2", "")

    # Jack agreement which came later
    if 'J_' in x:
        x = x = x.replace("[J_", "")
        x = x = x.replace("]", "")
    return x


first = do.copy()

del first['PR_url'], first['Commit_url'], first['1stResolve'], first['2ndResolve']

types = []
for c in first.columns:
    first[c] = first[c].apply(cleanFor1Res)
    # checking
    types.append(list(first[c].unique()))

print(types)

# %%

new_data = pd.DataFrame()
for i, row in first.iterrows():  # iterate rows
    rater_names = set()
    for c in first.columns:
        rater_names.update(row[c])

    """ this is bad sample"""
    if len(rater_names) < 2:
        print('heres where the issue lies', i)
        continue

    df = pd.DataFrame(row)
    df.columns = ['rater']
    for i, rater in enumerate(rater_names):
        df['rater'] = df.rater.str.replace(rater, 'Rater_{}'.format(i))

    df = df.transpose()

    new_data = new_data.append(df)

# %%
""" getting the first set score """

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
print(task.alpha())

# %%

""" second set 
Heuristic:
    get only the agreement part!
    remove the single ones!
"""


def secondClean(x):
    # WTF! is this, removing!
    if 'J_' in x:
        x = ""

    x = x.replace(' ', "")
    x = x.replace('2', 'AB')
    # remove disagreement ones
    if '(d)' in x:
        x = ""

    # if accepted then we give temp var, AB
    if '(a)' in x:
        x = 'AB'
    # weird stuff
    if 'J_' in x:
        x = x = x.replace("[J_", "")
        x = x = x.replace("]", "")

    if len(x) == 1:  # remove single ones with no majority score
        x = ""
    return x


second = do.copy()

del second['PR_url'], second['Commit_url'], second['1stResolve'], second['2ndResolve']

types = []
for c in second.columns:
    second[c] = second[c].apply(secondClean)
    # checking
    types.append(list(second[c].unique()))
print(types)

# %%
new_data = pd.DataFrame()
for i, row in second.iterrows():  # iterate rows
    rater_names = set()
    for c in second.columns:
        rater_names.update(row[c])

    """ this is bad sample"""
    if len(rater_names) < 2:
        print('here`s where the 2+ coders lie', i + 2)

    df = pd.DataFrame(row)
    df.columns = ['rater']
    for i, rater in enumerate(rater_names):
        df['rater'] = df.rater.str.replace(rater, 'Rater_{}'.format(i))

    df = df.transpose()
    new_data = new_data.append(df)

new_data = new_data.reset_index(drop=True)

# %%
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
print(task.alpha())

# this is the final!
new_data.to_csv(dir + '../upstream_processed.csv')
