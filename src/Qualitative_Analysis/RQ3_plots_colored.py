#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 10:17:48 2021
@author: aadityabhatia
"""

import numpy as np
import pandas as pd

"""merging with upstream and getting final dfs for plotting"""

dir_ = 'src/Qualitative Analysis/'
do = pd.read_csv(dir_ + 'downstream_processed.csv')
up = pd.read_csv(dir_ + 'upstream_processed.csv')

do = do.fillna("")
up = up.fillna("")


# %% transposing to get in right format

def getTranspose(df):
    new_df = pd.DataFrame(columns=['row_id', 'code'])
    for i, row in df.iterrows():
        is_code = []
        for c in df.columns:
            if row[c] != "":
                is_code.append(c)

        new_df.loc[len(new_df)] = [i, " ".join(is_code)]

    return new_df


downstream = getTranspose(do)
upstream = getTranspose(up)

# %%  getting the value for a specific code
code = 'evaluation_code_change'

for i, c in enumerate(up.columns):
    if code in c:
        print("yes in upstream", c, 'at', i)
for i, c in enumerate(do.columns):
    if code in c:
        print("yes in downstream", c, 'at', i)

print('UPSTREAM count of ', code, len(upstream[upstream['code'].str.contains(code)]))
print('DOWN STREAM count of ', code, len(downstream[downstream['code'].str.contains(code)]))

# %%
IMPLEMENTATION = ['platform', 'feature']
MAINTAINANCE = ['cross', 'accuracy|performance', 'debug', 'preprocessing', 'maint', 'param', 'model|training',
                'bug fix']
MODULE_MANAGEMENT = ['adding_regenerated code files', 'remove module', 'move module', 'add module']
DEPENDENCY_MANAGEMENT = ['remove package', 'update', 'add package']
NON_FCT_SC_CHNG = ['token replace', 'indent', 'refactor', 'clean up']
SCS_MNGMNT = ['versioning', 'change_of_file_permissi', 'source control', 'merge']
META_PROG = ['internationalization|internationalization', 'sharing', 'evaluation_code_change', 'testing',
             'understanding', 'build/config', 'documentation']
DATA = ['program data', 'input data', 'output data']
LEGAL = ["licence"]

types = LEGAL + DEPENDENCY_MANAGEMENT + SCS_MNGMNT + DATA + MODULE_MANAGEMENT + \
        IMPLEMENTATION + NON_FCT_SC_CHNG + \
        META_PROG + MAINTAINANCE

labels = [
    # LEGAL
    'License',

    # Dependency manamgenet
    'Remove Package', 'Update Package', 'Add Package',

    # SCS_MNGMNT
    'Versioning', 'File permission', 'Source Control', 'Merge',

    # DATA
    'Program Data', 'Input Data', 'Output Data',

    # MODULE_MANAGEMENT
    'Add Regenerated Module', 'Remove Module', 'Move Module', 'Add Module',

    # implementation
    'Platform', 'Feature',

    # MISC
    # 'Sharing', 'Comprehension',	'Param Tuning',

    # NON_FCT_SC_CHNG
    'Token Replace', 'Indent', 'Refactor', 'Cleanup',

    # META_PROG
    'Internationalization', 'Sharing', 'Change Evaluation', 'Testing', 'Comprehension', 'Build/Config', 'Documentation',

    # MAINTENANCE
    'Cross Cutting Concern', 'Model performance', 'Debug', 'Pre-processing', 'Maintenance', 'Param Tuning',
    'Model Training', 'Bug Fix',
]

""" final validation check to see if I missed any cols 
temp_df = pd.DataFrame()
temp_df['cols'] = list(up.columns) + list(do.columns)
for t in types:
    temp_df.loc[temp_df.cols.str.contains(t), 'new'] = 1
print(temp_df[temp_df.new.isna()].cols.to_list())
"""

# THIS IS FOR MULTIPLE COLOR Plotting

implementation_lst_U = []
implementation_lst_D = []

maintenance_lst_U = []
maintenance_lst_D = []

module_lst_U = []
module_lst_D = []

dependency_lst_U = []
dependency_lst_D = []

non_fsc_lst_U = []
non_fsc_lst_D = []

scsmgmnt_lst_U = []
scsmgmnt_lst_D = []

meta_lst_U = []
meta_lst_D = []

data_lst_U = []
data_lst_D = []

misc_lst_U = []
misc_lst_D = []

legal_lst_U = []
legal_lst_D = []

for t in types:
    print("processing for ", t, '>>>>>>.....')
    do_count = len(downstream[downstream.code.str.contains(t)])
    do_pct = round(do_count / (len(downstream)), 3) * 100

    up_count = len(upstream[upstream.code.str.contains(t)])
    up_pct = round(up_count / (len(upstream)), 3) * 100

    if t in (LEGAL):
        legal_lst_U.append(up_pct)
        legal_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        continue

    elif t in set(IMPLEMENTATION):
        implementation_lst_U.append(up_pct)
        implementation_lst_D.append(-1 * do_pct)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue
    elif t in set(MAINTAINANCE):
        maintenance_lst_U.append(up_pct)
        maintenance_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue
    elif t in (MODULE_MANAGEMENT):
        module_lst_U.append(up_pct)
        module_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue
    elif t in (DEPENDENCY_MANAGEMENT):
        dependency_lst_U.append(up_pct)
        dependency_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue
    elif t in (NON_FCT_SC_CHNG):
        non_fsc_lst_U.append(up_pct)
        non_fsc_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue
    elif t in (SCS_MNGMNT):
        scsmgmnt_lst_U.append(up_pct)
        scsmgmnt_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue

    elif t in (META_PROG):
        meta_lst_U.append(up_pct)
        meta_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue
    elif t in (DATA):
        data_lst_U.append(up_pct)
        data_lst_D.append(-1 * do_pct)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)
        legal_lst_U.append(0)
        legal_lst_D.append(0)
        continue


    else:
        print("WEIRD INPUT", t)
        implementation_lst_U.append(0)
        implementation_lst_D.append(0)
        maintenance_lst_U.append(0)
        maintenance_lst_D.append(0)
        module_lst_U.append(0)
        module_lst_D.append(0)
        dependency_lst_U.append(0)
        dependency_lst_D.append(0)
        non_fsc_lst_U.append(0)
        non_fsc_lst_D.append(0)
        scsmgmnt_lst_U.append(0)
        scsmgmnt_lst_D.append(0)
        meta_lst_U.append(0)
        meta_lst_D.append(0)
        data_lst_U.append(0)
        data_lst_D.append(0)
        misc_lst_U.append(0)
        misc_lst_D.append(0)

ind = np.arange(len(labels))
if len(ind) != len(misc_lst_U):
    print("BOO HOO!.. RECHECK")

# %%

"""
Final plotting
"""

import matplotlib.pyplot as plt
import matplotlib

# this was for TSE
# matplotlib.rcParams.update({'font.size': 12})

# this is now for EMSE single page
matplotlib.rcParams.update({'font.size': 16})

fig, ax = plt.subplots(figsize=(15, 8))
width = 0.4

ax.bar(ind, implementation_lst_U, width, color='plum')
ax.bar(ind, implementation_lst_D, width, label='Implementation', color='violet')

ax.bar(ind, maintenance_lst_U, width, color='slateblue')
ax.bar(ind, maintenance_lst_D, width, label='Maintenance', color='darkslateblue')

ax.bar(ind, module_lst_U, width, color='lightskyblue')
ax.bar(ind, module_lst_D, width, label='Module Mgmnt.', color='dodgerblue')

ax.bar(ind, dependency_lst_U, width, color='gold')
ax.bar(ind, dependency_lst_D, width, label='Dep. Mgmnt.', color='goldenrod')

ax.bar(ind, non_fsc_lst_U, width, color='peru')
ax.bar(ind, non_fsc_lst_D, width, label='Non Fsc.', color='chocolate')

ax.bar(ind, scsmgmnt_lst_U, width, color='lime')
ax.bar(ind, scsmgmnt_lst_D, width, label='Scs. Mgmnt.', color='limegreen')

ax.bar(ind, meta_lst_U, width, color='darkcyan')
ax.bar(ind, meta_lst_D, width, label='Meta', color='darkslategrey')

ax.bar(ind, data_lst_U, width, color='indianred')
ax.bar(ind, data_lst_D, width, label='Data', color='brown')

ax.bar(ind, misc_lst_U, width, color='dimgray')
ax.bar(ind, misc_lst_D, width, label='Misc.', color='black')

ax.bar(ind, legal_lst_U, width, color='blue')
ax.bar(ind, legal_lst_D, width, label='Legal.', color='blue')

# removing the negative in the y axis
ticks = ax.get_yticks()
ax.set_yticklabels([str(abs(tick)) + '%' for tick in ticks])
# ax.yaxis.set_major_formatter(mtick.PercentFormatter())


ax.set_ylabel('Percent of samples')
ax.legend()
ax.set_xticks(ind)
ax.set_xticklabels(labels, rotation=90)

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# this is for EMSE
plt.legend(bbox_to_anchor=(0.98, 1))  # legend outside

fig.tight_layout()
fig.savefig('../plots/upvsdown.pdf', dpi=3000)

# %%
count = 0
for t in DEPENDENCY_MANAGEMENT:
    count += len(upstream[upstream.code.str.contains(t)])
print(count)
# %%
# now we just print the numbers for downstream to report in the paper

a = pd.DataFrame(columns=[0, 1])
for t in types:
    do_count = len(downstream[downstream.code.str.contains(t)])
    do_pct = round(do_count / (len(downstream)) * 100, 1)
    print(t, do_pct)

    a.loc[len(a)] = [t, do_pct]

a = a.sort_values(by=[1], ascending=0)

# %%

""" second plot with Hindle"""

imple = 0.41
main = 0.1
mod_man = 0.29
dep = 0
non = 0.2
scs = 0.15
meta_prog = 0.32
data = 0
legal = 0.05

hindle_lst = [legal, dep, scs, data, mod_man,
              imple, non,
              meta_prog, main]

all_ = [LEGAL, DEPENDENCY_MANAGEMENT, SCS_MNGMNT, DATA, MODULE_MANAGEMENT,
        IMPLEMENTATION, NON_FCT_SC_CHNG,
        META_PROG, MAINTAINANCE]

all_labels = ["Legal", "Dependency\nManagement", "Source\nManagement", "Data", "Module\nManagement",
              "Implementation", "Non-Functional\nSource Change",
              "Meta\nProgram", "Maintenance"]

bhatia_lst = []
for type_ in all_:
    all_type_sum = 0
    for t in type_:
        do_count = len(downstream[downstream.code.str.contains(t)])
        up_count = len(upstream[upstream.code.str.contains(t)])

        # up_pct = round(up_count / len(upstream), 3)
        # do_pct = round(do_count / len(downstream), 3)
        # all_pct = all_pct + up_pct + do_pct
        ratio = (up_count + do_count) / (len(upstream) + len(downstream))
        ratio = round(ratio, 3)

        all_type_sum = all_type_sum + ratio

    bhatia_lst.append(all_type_sum)

print('Hindle sum:', sum(hindle_lst))
print('Bhatia sum:', sum(bhatia_lst))

print('proportion of maintenance', bhatia_lst[-1] / hindle_lst[-1])

width = 0.4
ind = np.arange(len(all_labels))

fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(ind + width / 2, bhatia_lst, width, label='This Study', color='black')
ax.bar(ind - width / 2, hindle_lst, width, label='Hindle et al.', color='silver')

ticks = ax.get_yticks()
ax.set_ylabel('Proportion of Change Types')
ax.legend()
ax.set_xticks(ind)
ax.set_xticklabels(all_labels, rotation=90)
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
fig.tight_layout()
fig.savefig('../plots/hindle_vs_bhatia.pdf', dpi=3000)
