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
from tkinter import simpledialog
import sys
import os

def data_from_file(file=None):
    if file==None:
        root = tk.Tk()
        root.withdraw()
        try:
            file = filedialog.askopenfilename(parent=root,
                                              filetypes=[('Text files',
                                                          '*.txt')])
            file = os.path.abspath(file)
        except FileNotFoundError:
            sys.exit()
            
        print(file)
        data = pd.read_csv(file,delimiter='\t')
        
        mass_valid = False
        while not(mass_valid):
            active_mass_input = simpledialog.askstring(parent=root,
                                       title="Active Mass",
                                       prompt="Enter Active Loading (mg):",
                                       initialvalue=8)
            mass_valid = check_valid_mass(active_mass_input)
            
            if not(mass_valid):
                tk.messagebox.showerror(title=None, 
                                        message="Enter a valid number!")
        
        active_mass = float(active_mass_input) / 1000
    
    return file,data,active_mass

def check_valid_mass(input_str):
    try:
        val = float(input_str)
    except ValueError:
        return False
    except TypeError:
        sys.exit()
    if val < 0:
        return False
    else:
        return True

def parse_data(data):
    
    if 'Ecell/V' in data:
        potential = data.loc[:,'Ecell/V']
    elif 'E /V' in data:
        potential = data.loc[:,'E /V']
    else:
        potential = 'NaN'
    print(potential)

    if '<I>/mA' in data:
        current = data.loc[:,'<I>/mA']
    elif 'I /mA' in data:
        current = data.loc[:,'I /mA']
    else:
        current = 'NaN'
    print(current)
    
    if 'time/s' in data:
        time = data.loc[:,'time/s']
    elif 'time /s' in data:
        time = data.loc[:,'time /s']
    else:
        time = 'NaN'
    print(time)
    
    return potential,time,current

def current_thresholds(current,rel_cutoff=0.98):
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
    
    if pos_count > neg_count:
        pos_cycle_no[pos_cycle_no > neg_count] = np.nan
        pos_count = neg_count
    elif pos_count < neg_count:
        neg_cycle_no[neg_cycle_no > pos_count] = np.nan
        neg_count = pos_count
 
    print("Number of neg cycles = %d \nNumber of pos cycles = %d" % (
        np.nanmax(neg_cycle_no),np.nanmax(pos_cycle_no)))  
 
    return pos_count,neg_count,pos_cycle_no,neg_cycle_no

# Here we need to create the value of capacity
# Capacity = time*current (mAs) / 3600 (mAh) / active mass (g) = mAh g^-1

def create_data_frame(file=None):    
    
    file,data,active_mass = data_from_file(file)
       
    (potential,
     time,current) = parse_data(data)
       
#    grav_capacity = capacity / active_mass
          
    is_pos,is_neg = current_thresholds(current,0.98)
   
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
        cyc_current = np.array(current[pos_cycle_no==cn+1].values,ndmin=1).T
        cyc_capacity = (cyc_time*cyc_current)/(3600*active_mass)        
        
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
        cyc_current = np.array(current[neg_cycle_no==cn+1].values,ndmin=1).T
        cyc_capacity = -1*(cyc_time*cyc_current)/(3600*active_mass)
        
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
        buffer = np.zeros(int(round(max_length)))*np.nan
        orig_len = np.max(np.shape(all_data[col]))
        buffer[0:orig_len] = all_data[col]
        all_data[col] = buffer
    
    save_dir = file[0:-4] + "_OUTPUTS"
    try:
        os.mkdir(save_dir)
    except FileExistsError:
        pass
    
    filename = os.path.basename(file)
    out_df = pd.DataFrame.from_dict(all_data,orient="columns")
    
    out_df.to_csv(os.path.join(save_dir,"%s%s" % (filename[0:-3],'csv') ), index = True)  
    
    return out_df,filename,save_dir,pos_count,neg_count

def create_cycles_seperate(out_df, save_dir):
    for i in range(len(out_df.columns)//6):
        match_C = '(C' + str(i+1) + ')'
        current_charge_cols = [col for col in out_df.columns if match_C in col]
        match_D = '(D' + str(i+1) + ')'
        current_discharge_cols = [col for col in out_df.columns if match_D in col]
        usecols = current_charge_cols + current_discharge_cols
        Cycle_x = out_df[usecols]
        Cycle_x.to_csv(os.path.join(save_dir,"Cycle_%d.csv" % (i+1)), index = True)

if __name__ == "__main__":

    out_df,file,save_dir,_,_ = create_data_frame()
    

            
            
