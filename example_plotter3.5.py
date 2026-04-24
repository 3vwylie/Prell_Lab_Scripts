# -*- coding: utf-8 -*-
"""
Created on Wed Dec  3 09:10:46 2025

@author: Austin

Edited on Wed Feb 11 10:24:20 2026

@editor: Rohan
"""


import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
#import glob
import pandas as pd
import argparse
parser = argparse.ArgumentParser(
    prog='python example_plotter3.5.py',
    description='''Given a txt file, plot dG, dH, dS averaged across replicates''')
parser.add_argument('startfile')
parser.add_argument('endfile', nargs= '?', default = None)
parser.add_argument('-m', '--mode', type = str, choices=['charge','ligand'], default = 'charge')
parser.add_argument('-d', '--difference', type = bool, choices=[True,False], default = False)
# difference argument is currently nonfunctional with charge vs bound delineations
parser.add_argument('-f', '--features', nargs = '?', default=2, type=int) #set the number of features
#parser.add_argument('dHdS_sep', choices = [True, False] default = False)
args = parser.parse_args()
if args.difference:
    if args.endfile is None:
        parser.error("endfile is required when --difference is True")

for i, fname in enumerate([f'{args.startfile}']): #####################
#for i, fname in enumerate('ConA20CIU_Nonhockey.txt'):
    # if '105 percent' in fname:
        # continue
    # trap_type = fname.split('\\')[1][:-8]
    # print(trap_type)
    keys = np.loadtxt(fname, delimiter=',', dtype='str')[0][1:]
    value = np.float64
    dtypes = dict.fromkeys(keys, value)
    spa_results = pd.read_csv(fname, skiprows=lambda x: (x != 0) and not x % 2, delimiter=', ')#, dtype=dtypes)
    spa_results.replace(' nan',0.0, inplace=True)
    spa_results.fillna(0.0, inplace=True)
    files = spa_results['infile'].to_numpy()

    def extract_infiles(infile):
        for idx in range(len(infile.split('/'))):
            if '.txt' in infile.split('/')[idx]:
                return infile.split('/')[idx]
            else: continue
    #This was created for differing amounts of nested files
    
    replicates = np.array([extract_infiles(v)[-8].upper() for v in files])
    names = np.array([extract_infiles(v)[:-7] for v in files])
    spa_results['Replicate'] = replicates
    spa_results['infile'] = names
    spa_results.sort_values(['infile', 'Replicate'], inplace=True)
    start_features_dict = {}
    for feat in range(1,args.features+1):
        if args.mode == 'charge':
            # print(spa_results['infile'])
            mincharge = min([int(file[file.index('CIU')-3:file.index('CIU')-1]) for file in spa_results['infile']])
            maxcharge = max([int(file[file.index('CIU')-3:file.index('CIU')-1]) for file in spa_results['infile']])
            #automatically detects the max and min charges-- could accept this as an argument instead?
            #assumes {charge}_CIU format
            for charge in range(mincharge, maxcharge+1):
                start_features_dict[f'z{charge}_feat{feat}_df'] = spa_results[spa_results['infile'].str.contains(f'{charge}_CIU_{feat}')]
        elif args.mode == 'ligand':
            maxbound = max([int(file[file.index('b')-1]) for file in spa_results['infile']])
            #automatically detects the max number of ligands bound-- could accept this as an argument instead?
            #will run into issues if there is a b present elsewhere in file
            for bound in range(maxbound+1):
                start_features_dict[f'feat{feat}_{bound}b_df'] = spa_results[spa_results['infile'].str.contains(f'{feat}_{bound}b')]


if args.endfile:
    for i, fname in enumerate([f'{args.endfile}']): #####################
    #for i, fname in enumerate('ConA20CIU_Nonhockey.txt'):
        # if '105 percent' in fname:
            # continue
        # trap_type = fname.split('\\')[1][:-8]
        # print(trap_type)
        keys = np.loadtxt(fname, delimiter=',', dtype='str')[0][1:]
        value = np.float64
        dtypes = dict.fromkeys(keys, value)
        spa_results = pd.read_csv(fname, skiprows=lambda x: (x != 0) and not x % 2, delimiter=', ')#, dtype=dtypes)
        spa_results.replace(' nan',0.0, inplace=True)
        spa_results.fillna(0.0, inplace=True)
        files = spa_results['infile'].to_numpy()
        replicates = np.array([v.split('/')[1][-8].upper() for v in files])
        names = np.array([v.split('/')[1][:-7] for v in files])
        spa_results['Replicate'] = replicates
        spa_results['infile'] = names
        spa_results.sort_values(['infile', 'Replicate'], inplace=True)

        end_features_dict = {}
        for feat in range(1,args.features+1):
            if args.mode == 'charge':
                mincharge = min([int(file[file.index('z')+1:file.index('z')+3]) for file in spa_results['infile']])
                maxcharge = max([int(file[file.index('z')+1:file.index('z')+3]) for file in spa_results['infile']])
                #automatically detects the max and min charges-- could accept this as an argument instead?
                #will run into issues if there is a z present elsewhere in file
                for charge in range(mincharge,maxcharge+1):
                    end_features_dict[f'z{charge}_feat{feat}_df'] = spa_results[spa_results['infile'].str.contains(f'z{charge}_CIU_{feat}b')]
            elif args.mode == 'ligand':
                maxbound = max([int(file[file.index('b')-1]) for file in spa_results['infile']])
                #automatically detects the max number of ligands bound-- could accept this as an argument instead?
                #will run into issues if there is a b present elsewhere in file
                for bound in range(maxbound+1):
                    end_features_dict[f'feat{feat}_{bound}b_df'] = spa_results[spa_results['infile'].str.contains(f'{feat}_{bound}b')]

def average_df(dataframe, ion='BSA'):

    if 'BSA' in ion:
        dHs = dataframe['dH'].to_numpy()[dataframe['dS'].to_numpy() < 800]
        dSs = dataframe['dS'].to_numpy()[dataframe['dS'].to_numpy() < 800]
        # dGs = dataframe['dG'].to_numpy()[dataframe['dG'].to_numpy() > 78]
        Teffs = dataframe['Teff'].to_numpy()[dataframe['dS'].to_numpy() < 800]
        
        dHs_err = dataframe['errdH'].to_numpy()[dataframe['dS'].to_numpy() < 800]
        dSs_err = dataframe['errdS'].to_numpy()[dataframe['dS'].to_numpy() < 800]
        dGs_err = dataframe['errdG'].to_numpy()[dataframe['dS'].to_numpy() < 800]
        
        # print(dHs)
    else:
        dHs = dataframe['dH'].to_numpy()
        dSs = dataframe['dS'].to_numpy()
        # dGs = dataframe['dG'].to_numpy()
        Teffs = dataframe['Teff'].to_numpy()
        
        dHs_err = dataframe['errdH'].to_numpy()
        dSs_err = dataframe['errdS'].to_numpy()    
        dGs_err = dataframe['errdG'].to_numpy()
    
    # print(f'Ion is: {ion} and length of dH array is: {len(dHs)}')
    
    dGs = dHs - dSs*Teffs/1000
    Teffs_err = Teffs*0.05
    
    dHs_mean = np.mean(dHs)
    dHs_std = np.std(dHs)
    dHs_quad_errs = np.sum(dHs_err**2)
    
    
    dSs_mean = np.mean(dSs)
    dSs_std = np.std(dSs)
    dSs_quad_errs = np.sum(dSs_err**2)
    
    dGs_mean = np.mean(dGs)
    dGs_std = np.std(dGs)
    dGs_quad_errs = np.sum(dGs_err**2)
    
    
    Teffs_mean = np.mean(Teffs)
    Teffs_std = np.std(Teffs)
    Teffs_quad_errs = np.sum(Teffs_err**2)
    
    ions = [ion]
    
    dH_toterr = np.sqrt((dHs_std**2 + 0.05*dHs_mean))#/9)
    dS_toterr = np.sqrt((dSs_std**2 + 0.05*dSs_mean))#/9)
    
    Teff_toterr = np.sqrt((Teffs_std**2 + Teffs_quad_errs))#/9)
    # print(dH_toterr)
    # print(dS_toterr/1000)
    # print(Teff_toterr/1000)
    dG_toterr = np.sqrt(dGs_std**2 + dGs_mean*0.05)# + (Teff_toterr/Teffs_mean)**2))#/9)
    dGs_298 = dHs_mean - dSs_mean * 298 / 1000
    
    
    new_df = pd.DataFrame()
    new_df['Ions'] = ions
    new_df['dH'] = [dHs_mean]
    new_df['dH tot err'] = dH_toterr
    new_df['dH std'] = dHs_std
    new_df['dH quad err'] = dHs_quad_errs
    new_df['dS'] = dSs_mean
    new_df['dS tot err'] = dS_toterr
    new_df['dS std'] = dSs_std
    new_df['dS quad err'] = dSs_quad_errs
    new_df['dG'] = dGs_mean
    new_df['dG tot err'] = dG_toterr
    new_df['dG std'] = dGs_std
    new_df['dG quad err'] = dGs_quad_errs
    new_df['Temp'] = Teffs_mean
    new_df['dG_298'] = dGs_298
    
    new_df.sort_values(['Ions'], inplace=True)
    
    return new_df

def diff_df(dataframe1, dataframe2, ion = "ConA"):

    dHs1 = dataframe1['dH'].to_numpy()
    dSs1 = dataframe1['dS'].to_numpy()
    # dGs = dataframe['dG'].to_numpy()
    Teffs1 = dataframe1['Temp'].to_numpy()
    
    dHs_err1 = dataframe1['dH tot err'].to_numpy()
    dSs_err1 = dataframe1['dS tot err'].to_numpy()    
    dGs_err1 = dataframe1['dG tot err'].to_numpy()

    dHs2 = dataframe2['dH'].to_numpy()
    dSs2 = dataframe2['dS'].to_numpy()
    # dGs = dataframe['dG'].to_numpy()
    Teffs2 = dataframe2['Temp'].to_numpy()
    
    dHs_err2 = dataframe2['dH tot err'].to_numpy()
    dSs_err2 = dataframe2['dS tot err'].to_numpy()    
    dGs_err2 = dataframe2['dG tot err'].to_numpy()
    
    # print(f'Ion is: {ion} and length of dH array is: {len(dHs)}')
    
    dGs1 = dHs1 - dSs1*Teffs1/1000
    dGs2 = dHs2 - dSs2*Teffs2/1000
    
    dH_diffs = dHs1 - dHs2
    dH_diff_errs = (dHs_err1**2+dHs_err2**2)**0.5
    
    dS_diffs = dSs1 - dSs2
    dS_diff_errs = (dSs_err1**2+dSs_err2**2)**0.5
    
    dG_diffs = dGs1 - dGs2
    dG_diff_errs = (dGs_err1**2+dGs_err2**2)**0.5
    
    ions = [ion]

    dG_298_diffs = dH_diffs - dS_diffs * 298 / 1000
    
    
    diff_df = pd.DataFrame()
    diff_df['Ions'] = ions
    #new_df['Ions'] = 0 #had to set Ion name to a non-string or else subtracting gives an error
    diff_df['dH'] = dH_diffs
    diff_df['dH tot err'] = dH_diff_errs
    # new_df['dH std'] = dHs_std
    # new_df['dH quad err'] = dHs_quad_errs
    diff_df['dS'] = dS_diffs
    diff_df['dS tot err'] = dS_diff_errs
    # new_df['dS std'] = dSs_std
    # new_df['dS quad err'] = dSs_quad_errs
    diff_df['dG'] = dG_diffs
    diff_df['dG tot err'] = dG_diff_errs
    # new_df['dG std'] = dGs_std
    # new_df['dG quad err'] = dGs_quad_errs
    diff_df['Temp'] = Teffs1
    diff_df['dG_298'] = dG_298_diffs
    
    diff_df.sort_values(['Ions'], inplace=True)
    
    return diff_df

avg_dict = {}

if args.mode == 'charge':
    for charge in range(mincharge,maxcharge+1):
        if args.difference:
            for feat in range(1,args.features+1):
                avg_dict[f'feat{feat}_0b_df_avg'] = diff_df(average_df(start_features_dict[f'z{charge}_feat{feat}_df']),
                                                    average_df(end_features_dict[f'z{charge}_feat{feat}_df']))
        else:
            for feat in range(1,args.features+1):
                avg_dict[f'z{charge}_feat{feat}_df_avg'] = average_df(start_features_dict[f'z{charge}_feat{feat}_df'])
elif args.mode == 'ligand':
    for bound in range(maxbound+1):
        if args.difference:
            for feat in range(1,args.features+1):
                avg_dict[f'feat{feat}_0b_df_avg'] = diff_df(average_df(start_features_dict[f'feat{feat}_{bound}b_df']),
                                                    average_df(end_features_dict[f'feat{feat}_{bound}b_df']))
        else:
            for feat in range(1,args.features+1):
                avg_dict[f'feat{feat}_{bound}b_df_avg'] = average_df(start_features_dict[f'feat{feat}_{bound}b_df'])


fig, ax = plt.subplots(2, sharex=True)
fig2, ax2 = plt.subplots()
colors = cm.viridis(np.linspace(0, 0.8, args.features)) #redoing the colors to be based on args.features


def dHSG_plot(dfs_list,offset):
    '''given a list of dataframes, plot dH and dS values on one graph, dG values on another'''
    for j, df in enumerate(dfs_list):
        dHs = df['dH'].to_numpy()
        dHes = df['dH tot err']
        dSs = df['dS'].to_numpy()
        dSes = df['dS tot err']
        dGs = df['dG'].to_numpy()
        dGes = df['dG tot err']
        dG298s = df['dG_298']
        ions = df['Ions']

        for dH, dHe, dS, dSe, dG, dGe, ion, dG298 in zip(dHs, dHes, dSs, dSes, dGs, dGes, ions, dG298s):
            label = f'Transition {j+1}' if offset == 0 else None #only add a label for the first set of plots

            ax[0].errorbar(offset + j/8, dH, dHe, capsize=15, marker='o', markersize=15, linewidth=2, c=colors[j], label = label)
            ax[1].errorbar(offset + j/8, dS, dSe, capsize=15, marker='o', markersize=15, linewidth=2, c=colors[j])
            
            ax2.errorbar(offset + j/8, dG, dGe, capsize=15, marker='o', markersize=15, linewidth=2, c=colors[j], label = label)
            #ax2[1].errorbar(0 + j/8, dG298, dGe, capsize=25, marker='o', markersize=25, linewidth=2, c='k')

if args.mode == 'charge':
    xticks = [x for x in range(maxcharge-mincharge+1)]
    labels = [str(x)+'+' for x in range(mincharge,maxcharge+1)]
    for charge in range(mincharge,maxcharge+1):
        dHSG_plot([avg_dict[key] for key in avg_dict.keys() if f'z{charge}' in key],charge-mincharge)
elif args.mode == 'ligand':
    xticks = [x for x in range(maxbound+1)]
    labels = [str(x) for x in range(maxbound+1)]
    for bound in range(maxbound + 1):
        dHSG_plot([avg_dict[key] for key in avg_dict.keys() if f'{bound}b' in key],bound)


dHs_array = ([avg_dict[key]['dH'].to_numpy() for key in avg_dict.keys()])
dSs_array = ([avg_dict[key]['dS'].to_numpy() for key in avg_dict.keys()])
dGs_array = ([avg_dict[key]['dG'].to_numpy() for key in avg_dict.keys()])
dHs_range = np.max(dHs_array) #we want dH to go all the way to 0
dSs_range = np.max(dSs_array) - np.min(dSs_array)
dGs_range = np.max(dGs_array) #we want dG to go all the way to 0
#Defines range of dH, dS, and dG values to determine ticker.MultipleLocator for dH dS and dG graphs
dH_ticker = round(dHs_range/25)*5 #Divide by 5, then divide by 5, math.ceil, and multiply by 5
dS_ticker = round(dSs_range/25)*5 #This divides the number by 5, then rounds to the nearest 5
dG_ticker = round(dGs_range/25)*5

ax[0].set_xticks(xticks,labels)
ax[0].tick_params(axis='both', which='major', labelsize=15)
ax[0].tick_params(axis='y', which='major', pad=10)
ax[0].yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(dH_ticker))
# ax[0].minorticks_on()
ax[0].tick_params(axis='y', which='minor', length=8, width=1)
ax[0].tick_params(axis='x', which='minor', length=0, width=0)
if args.difference:
    ax[0].set_title(f'IonSPA difference results', fontsize=30)
    ax[0].axhline(y=0, color='k', linestyle = '--')
    ax[0].set_ylabel(r'$\Delta \Delta H^{\ddag}$ (kJ/mol)',fontsize=20)
else:    
    ax[0].set_title(f'IonSPA results for {args.startfile[:-4]}', fontsize=30)
    ax[0].set_ylabel(r'$\Delta H^{\ddag}$ (kJ/mol)',fontsize=20)
ax[0].set_ylim(0,)
# ax[0].set_xlim(0,275)
ax[0].legend()
# ax[0].legend(fontsize=30)

ax[1].set_xticks(xticks,labels)
ax[1].tick_params(axis='both', which='major', labelsize=15)
ax[1].tick_params(axis='y', which='major', pad=10)
ax[1].yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(dS_ticker))
# ax[1].minorticks_on()
ax[1].tick_params(axis='y', which='minor', length=8, width=1)
ax[1].tick_params(axis='x', which='minor', length=0, width=0)
if args.mode == 'charge':
    ax[1].set_xlabel(r'Charge State',fontsize=20)
elif args.mode == 'ligand':
    ax[1].set_xlabel(r'Number of Bound Ligands',fontsize=20)
ax[1].axhline(y=0, color='k', linestyle = '--')
if args.difference:
    ax[1].set_ylabel(r'$\Delta \Delta S^{\ddag}$ (J/mol*K)',fontsize=20)
else:
    ax[1].set_ylabel(r'$\Delta S^{\ddag}$ (J/mol*K)',fontsize=20)
# ax[1].set_title(r'IonSPA results for entropy on Synapt', fontsize=75)
#ax[1].set_ylim(0,600)
# ax4.set_xlim(0,6)
# ax2.legend()
# ax2.legend(fontsize=30)

ax2.set_xticks(xticks,labels, fontsize=40)
ax2.tick_params(axis='both', which='major', labelsize=15)
ax2.yaxis.set_major_locator(matplotlib.ticker.MultipleLocator(dG_ticker))
ax2.set_ylim(0,)
ax2.tick_params(axis='y', which='major', pad=10)
# ax[2].minorticks_on()
ax2.tick_params(axis='y', which='minor', length=8, width=1)
ax2.tick_params(axis='x', which='minor', length=0, width=0)
if args.mode == 'charge':
    ax2.set_xlabel(r'Charge State',fontsize=20)
elif args.mode == 'ligand':
    ax2.set_xlabel(r'Number of Bound Ligands',fontsize=20)

if args.difference:
    ax2.set_title(f'IonSPA difference results', fontsize=30)
    ax2.axhline(y=0, color='k', linestyle = '--')
    ax2.set_ylabel(r'$\Delta \Delta G^{\ddag}$ (kJ/mol)',fontsize=20)
else:    
    ax2.set_title(f'IonSPA results for {args.startfile[:-4]}', fontsize=30)
    ax2.set_ylabel(r'$\Delta G^{\ddag}$ (kJ/mol)',fontsize=20)

ax2.legend()

plt.show()






























































