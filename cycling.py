# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 22:46:50 2020

@author: lukas Rier
lukasrier@outlook.com
"""
import numpy as np
import matplotlib.pyplot as plt
# from scipy.signal import find_peaks
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# Setting up file dialog
root = tk.Tk()
file_path = filedialog.askopenfilename(parent=root)

################
# Ask for user input TODO
# active_mass = float(input("Acitve loading (g):"))
active_mass = 0.008
################
root.withdraw()
print(file_path)

data = pd.read_csv(file_path,delimiter='\t')

potential = data.loc[:,'Ecell/V']
current = data.loc[:,'<I>/mA']
capacity = data.loc[:,'Capacity/mA.h'] / active_mass
cycle_no = data.loc[:,'cycle number']
time = data.loc[:,'time/s']

# # plt.plot(time,current)
# kernel = [0,-0.5,-1,-0.5,0,0.5,1,0.5,0]
# current_edges = -1*np.convolve(current,kernel,mode='same')


plt.figure()
plt.plot(time,current)
# plt.plot(time,current_edges)

posthresh = 0.01 * np.max(current)
negthresh = 0.01 * np.min(current)

# plt.figure()
# plt.plot(time,current)
# plt.plot(time,posthresh*np.ones(np.shape(time)))
# plt.plot(time,negthresh*np.ones(np.shape(time)))

pos_cycles = current > posthresh
neg_cycles = -1 * (current < negthresh)
is_pos = pos_cycles != 0
is_neg = neg_cycles != 0


# plt.figure()
# plt.plot(time,current)
# plt.plot(time[is_pos],0*pos_cycles[is_pos],'.')
# plt.plot(time[is_neg],0*neg_cycles[is_neg],'.')


pos_edge = np.convolve(is_pos,[1,-1],mode='same')
neg_edge = np.convolve(is_neg,[1,-1],mode='same')


# negdiff = np.append(np.diff(is_neg),0)

# plt.figure()
# plt.plot(time,posdiff)
# plt.plot(time,0.1*(pos_edge==1),'*')
# plt.plot(time,0.1*(neg_edge==1),'*')

# plt.plot(time,-1*negdiff)
# plt.plot(time,current)

# Cycle along all samples and get cycle number v time
pos_cycle_no = np.zeros(time.shape)*np.nan
pos_count = 0
neg_cycle_no = np.zeros(time.shape)*np.nan
neg_count = 0

# posfirst = 0
# negfirst = 0
for i,t in enumerate(time):
    incycle = is_pos[i] | is_neg[i]
    if is_pos[i]:
        if pos_edge[i]==1:
            pos_count += 1
            #posfirst = not(negfirst) and not(posfirst)
        pos_cycle_no[i] = pos_count
    
    if is_neg[i]:
        if neg_edge[i]==1:
            neg_count += 1
            #negfirst = not(negfirst) and not(posfirst)
        neg_cycle_no[i] = neg_count

# plt.plot(time,pos_cycle_no)
# plt.plot(time,neg_cycle_no)

print("Number of neg cycles = %d \nNumber of pos cycles = %d" % (neg_count,pos_count))       
    
count = min(neg_count,pos_count)

all_data = dict()

for cn in range(pos_count):
    exp_time = np.array(time[pos_cycle_no==cn+1].values,ndmin=1).T
    cyc_time = exp_time - exp_time[0]
    cyc_pot = np.array(potential[pos_cycle_no==cn+1].values,ndmin=1).T
    cyc_capacity = np.array(capacity[pos_cycle_no==cn+1].values,ndmin=1).T 
    
    ct_name = "Elapsed time/s (C" + str(cn+1) + ")"
    all_data[ct_name] = cyc_time
    
    cyc_pot_name = "Ecell/V (C" + str(cn+1) + ")"
    all_data[cyc_pot_name] = cyc_pot
    
    cyc_cap_name = "Capacity/mA.h.g^-1 (C" + str(cn+1) + ")"
    all_data[cyc_cap_name] = cyc_capacity
    
for cn in range(neg_count):
    exp_time = np.array(time[neg_cycle_no==cn+1].values,ndmin=1).T
    cyc_time = exp_time - exp_time[0]
    cyc_pot = np.array(potential[neg_cycle_no==cn+1].values,ndmin=1).T
    cyc_capacity = np.array(capacity[neg_cycle_no==cn+1].values,ndmin=1).T
    
    ct_name = "Elapsed time/s (D" + str(cn+1) + ")"
    all_data[ct_name] = cyc_time
    
    cyc_pot_name = "Ecell/V (D" + str(cn+1) + ")"
    all_data[cyc_pot_name] = cyc_pot
    
    cyc_cap_name = "Capacity/mA.h.g^-1 (D" + str(cn+1) + ")"
    all_data[cyc_cap_name] = cyc_capacity   
    
length = np.array([])

for col in all_data:    
    arr = all_data[col]
    sh = np.shape(arr)
    length = np.append(length,sh[0])
    
max_length = np.max(length)

for i,col in enumerate(all_data): 
    buffer = np.zeros(int(round(max_length)))*np.nan
    orig_len = np.max(np.shape(all_data[col]))
    buffer[0:orig_len] = all_data[col]
    all_data[col] = buffer
    

    
out_df = pd.DataFrame.from_dict(all_data,orient="columns")
# outdf_csv_data = out_df.to_csv("%s%s" % (file_path[0:-3],'csv'), index = True)

charge_cols = [col for col in out_df.columns if 'Capacity/mA.h.g^-1 (C' in col]
max_charge_cap = np.zeros((pos_count,1))
for i,col in enumerate(charge_cols):
    max_charge_cap[i]=np.max(out_df[col])
    print(max_charge_cap[i])
    
discharge_cols =  [col for col in out_df.columns if 'Capacity/mA.h.g^-1 (D' in col]
max_discharge_cap = np.zeros((neg_count,1))
for i,col in enumerate(discharge_cols):
    max_discharge_cap[i]=np.max(out_df[col])
    print(max_discharge_cap[i])
    
cycle_no = np.arange(1,pos_count+1)
    
plt.figure()
plt.plot(cycle_no, max_discharge_cap, 'x')
plt.plot(cycle_no,max_charge_cap, 'x')
plt.legend(["Discharge capacity", "Charge capacity"])
plt.xlabel("Cycle Number")
plt.ylabel("Capacity mAh g^-1)
plt.show()
# plt.close()