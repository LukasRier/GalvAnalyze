# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 20:16:32 2020

@author: lukas Rier
lukasrier@outlook.com
"""
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog

def data_from_file(file=None):
    if file==None:
        root = tk.Tk()
        file = filedialog.askopenfilename(parent=root)
        root.withdraw()
        print(file)
    
    data = pd.read_csv(file,delimiter='\t')
    return file,data

def parse_data(data):
    potential = data.loc[:,'Ecell/V']
    current = data.loc[:,'<I>/mA']
    capacity = data.loc[:,'Capacity/mA.h']
    cycle_no = data.loc[:,'cycle number']
    time = data.loc[:,'time/s']
    return potential,capacity,time,current,cycle_no

def current_thresholds(current,rel_cutoff=0.01):
    posthresh = rel_cutoff * np.max(current)
    negthresh = rel_cutoff * np.min(current)
    pos_cycles = current > posthresh
    neg_cycles = -1 * (current < negthresh)
    is_pos = pos_cycles != 0
    is_neg = neg_cycles != 0
    return is_pos,is_neg

def find_edges(is_pos,is_neg):
    pos_edge = np.convolve(is_pos,[1,-1],mode='same')
    neg_edge = np.convolve(is_neg,[1,-1],mode='same')
    return pos_edge,neg_edge
      
def get_cycle_counts(time,is_pos,is_neg):
    pos_edge,neg_edge = find_edges(is_pos,is_neg)
          
    pos_cycle_no = np.zeros(time.shape)*np.nan
    pos_count = 0
    neg_cycle_no = np.zeros(time.shape)*np.nan
    neg_count = 0
    
    for i,t in enumerate(time):
        if is_pos[i]:
            if pos_edge[i]==1:
                pos_count += 1
            pos_cycle_no[i] = pos_count
    
        if is_neg[i]:
            if neg_edge[i]==1:
                neg_count += 1
                neg_cycle_no[i] = neg_count
    print("Number of neg cycles = %d \nNumber of pos cycles = %d" % (neg_count,pos_count))       
 
    return pos_count,neg_count,pos_cycle_no,neg_cycle_no

def create_data_frame(file=None):    
    file,data = data_from_file(file)
    ######### TODO
    # active mass user input
    active_mass = 1
    
    (potential,capacity,
     time,current,cycle_no) = parse_data(data)
    
    capacity = capacity / active_mass
        
    is_pos,is_neg = current_thresholds(current,0.01)
   
    pos_edge,neg_edge = find_edges(is_pos,is_neg)
    
    (pos_count,neg_count,
     pos_cycle_no,neg_cycle_no) = get_cycle_counts(time,is_pos,is_neg)


    all_data = dict()

    time_head = "Elapsed time/s "
    potential_head = "Ecell/V "
    capacity_head = "Capacity/mA.h.g^-1 "
    for cn in range(pos_count):
        exp_time = np.array(time[pos_cycle_no==cn+1].values,ndmin=1).T
        cyc_time = exp_time - exp_time[0]
        cyc_pot = np.array(potential[pos_cycle_no==cn+1].values,ndmin=1).T
        cyc_capacity = np.array(capacity[pos_cycle_no==cn+1].values,ndmin=1).T 
        
        ct_name = time_head + "(C" + str(cn+1) + ")"
        all_data[ct_name] = cyc_time
        
        cyc_pot_name = potential_head + "(C" + str(cn+1) + ")"
        all_data[cyc_pot_name] = cyc_pot
        
        cyc_cap_name = capacity_head + "(C" + str(cn+1) + ")"
        all_data[cyc_cap_name] = cyc_capacity
    

    for cn in range(neg_count):
        exp_time = np.array(time[neg_cycle_no==cn+1].values,ndmin=1).T
        cyc_time = exp_time - exp_time[0]
        cyc_pot = np.array(potential[neg_cycle_no==cn+1].values,ndmin=1).T
        cyc_capacity = np.array(capacity[neg_cycle_no==cn+1].values,ndmin=1).T
        
        ct_name = time_head + "(D" + str(cn+1) + ")"
        all_data[ct_name] = cyc_time
        
        cyc_pot_name = potential_head + "(D" + str(cn+1) + ")"
        all_data[cyc_pot_name] = cyc_pot
        
        
        cyc_cap_name =  capacity_head + "(D" + str(cn+1) + ")"
        all_data[cyc_cap_name] = cyc_capacity   
    
    length = np.array([])
    
    for col in all_data:    
        arr = all_data[col]
        sh = np.shape(arr)
        length = np.append(length,sh[0])
        
    max_length = np.max(length)
    
    for i,col in enumerate(all_data): 
        buffer = np.zeros([round(max_length)])*np.nan
        orig_len = np.max(np.shape(all_data[col]))
        buffer[0:orig_len] = all_data[col]
        all_data[col] = buffer
    
        
    out_df = pd.DataFrame.from_dict(all_data,orient="columns")
    
    return out_df,file

if __name__ == "__main__":
    

    out_df,file_path = create_data_frame()

    outdf_csv_data = out_df.to_csv("%s%s" % (file_path[0:-3],'csv'), index = True)
    

            
            
