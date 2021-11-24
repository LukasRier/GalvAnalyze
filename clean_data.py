# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 20:16:32 2020

@authors: lukas Rier & Rory McNulty
lukasrier@outlook.com
"""
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import sys
import os
import matplotlib.pyplot as plt
import cycling_plots as cyc

def data_from_file(file=None,active_mass_input=None):
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
        
    if active_mass_input==None:
        mass_valid = False
    else:
        mass_valid = check_valid_mass(active_mass_input)
    while not(mass_valid):
        if not 'root' in locals():
            root = tk.Tk()
            root.lift()
        active_mass_input = simpledialog.askstring(parent=root,
                                   title="Active Mass",
                                   prompt="Enter Active Loading (mg):",
                                   initialvalue=8)
        mass_valid = check_valid_mass(active_mass_input)
        
        if not(mass_valid):
            tk.messagebox.showerror(title=None, 
                                    message="Enter a valid number!")
    
    if 'root' in locals():
        root.destroy()
        
    active_mass = float(active_mass_input) / 1000
    
    return file,data,active_mass

def check_valid_mass(input_str):
    try:
        val = float(input_str)
    except ValueError:
        return False
    except TypeError:
        # sys.exit()
        return False
    if val < 0:
        return False
    else:
        return True

def parse_data(data):
    
    if 'Ecell/V' in data:
        potential = data.loc[:,'Ecell/V']
    elif 'E /V' in data:
        potential = data.loc[:,'E /V']
    elif 'Ewe/V' in data:
        potential = data.loc[:,'Ewe/V']
    else:
        potential = 'NaN'
    print(potential)

    if '<I>/mA' in data:
        current = data.loc[:,'<I>/mA']
    elif 'I /mA' in data:
        current = data.loc[:,'I /mA']
    elif 'I/mA' in data:
        current = data.loc[:,'I/mA']
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

def const_current_thresh_diagnostic(current,posthresh,negthresh):
    import matplotlib.pyplot as plt
    plt.figure()
    ax = plt.subplot(111)
    ax.plot(current,'k')
    ax.plot(np.arange(1,len(current)+1),posthresh * np.ones((len(current))),'r')
    ax.plot(np.arange(1,len(current)+1),negthresh * np.ones((len(current))),'b')
    
def variable_current_thresh_diagnostic(current,thresh,in_cycle,absgrad):
    
    plt.figure()
    ax = plt.subplot(111)
    ax.plot(current,'k')
    ax.plot(thresh * np.ones((len(current))),'r')
    ax.plot(-1 *thresh * np.ones((len(current))),'b')
    
    plt.figure()
    ax = plt.subplot(111)
    ax.hist(current,bins=10)
    
    plt.figure()
    ax = plt.subplot(111)
    ax.plot(absgrad,'k')
    plt.title('absgrad')
    # ax.plot(in_cycle,'r--')
    ax.plot(in_cycle * np.sign(current),'r--')
        
def check_min_curr_correct(incycle_thresh):
    incycle_thresh_valid = False
    while not(incycle_thresh_valid):
        if not 'root' in locals():
            root = tk.Tk()
            root.lift()
        incycle_thresh_input = simpledialog.askstring(parent=root,
                                   title="Min current threshold",
                                   prompt="Desired current threshold (mA):",
                                   initialvalue=incycle_thresh)
        incycle_thresh_valid = check_valid_mass(incycle_thresh_input)
        
        if not(incycle_thresh_valid):
            tk.messagebox.showerror(title=None, 
                                    message="Enter a valid number!")
    
    if 'root' in locals():
        root.destroy()
    incycle_thresh = float(incycle_thresh_input)
    
    return incycle_thresh


def current_thresholds(current,rel_cutoff=0.98,is_constant=True):
    if is_constant:
        posthresh = rel_cutoff * np.max(current)
        negthresh = rel_cutoff * np.min(current)
        pos_cycles = current > posthresh
        neg_cycles = -1 * (current < negthresh)
        is_pos = pos_cycles != 0
        is_neg = neg_cycles != 0
        
        
        ## Diagnostic plots! uncomment if needed
        # const_current_thresh_diagnostic(current,posthresh,negthresh)
    else:
        absgrad = np.abs(find_edges(current))
        
        incycle_thresh = np.min(np.unique(absgrad[absgrad > 0]))
        
        incycle_thresh = check_min_curr_correct(incycle_thresh)
        in_cycle = absgrad < incycle_thresh
        
        #get rid of initial period
        if in_cycle[0] == 1:
            in_cycle[0] = 0
            st = 1
            while in_cycle[st] == 1:
                in_cycle[st] = 0
                st += 1
            print("removed ",st,"points from the beginning")
        
        ## Diagnostic plots! uncomment if needed
        # const_current_thresh_diagnostic(current,1,1)
        # variable_current_thresh_diagnostic(current,0,in_cycle,absgrad)
        
        
        signed_in_cycle = in_cycle * np.sign(current)
        is_pos = signed_in_cycle == 1
        is_neg = signed_in_cycle == -1
    return is_pos,is_neg

def find_edges(is_incycle):
    edge = np.convolve(is_incycle,[1,-1],mode='same')
    return edge
      
def get_cycle_counts(time,is_pos,is_neg):
    pos_edge,neg_edge = find_edges(is_pos),find_edges(is_neg)
          
    pos_cycle_no = np.zeros(time.shape)*np.nan
    pos_count = 0
    neg_cycle_no = np.zeros(time.shape)*np.nan
    neg_count = 0
    
    for i,t in enumerate(time):
        if is_pos[i]:
            if pos_edge[i]==1:
                pos_count += 1
                pos_cycle_no[i-2] = pos_count
            pos_cycle_no[i] = pos_count
    
        if is_neg[i]:
            if neg_edge[i]==1:
                neg_count += 1
                neg_cycle_no[i-2] = neg_count
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

def create_data_frame(file=None,active_mass=None,is_constant=True):    
    
    file,data,active_mass = data_from_file(file,active_mass)
       
    (potential,
     time,current) = parse_data(data)
       
#    grav_capacity = capacity / active_mass
          
    is_pos,is_neg = current_thresholds(current,0.98,is_constant)
   
    # pos_edge,neg_edge = find_edges(is_pos),find_edges(is_neg)
    
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
        
        cyc_cap_name = capacity_head + "(C" + str(cn+1) + ")"
        all_data[cyc_cap_name] = cyc_capacity
        
        cyc_pot_name = potential_head + "(C" + str(cn+1) + ")"
        all_data[cyc_pot_name] = cyc_pot
    

    for cn in range(neg_count):
        exp_time = np.array(time[neg_cycle_no==cn+1].values,ndmin=1).T
        cyc_time = exp_time - exp_time[0]
        cyc_pot = np.array(potential[neg_cycle_no==cn+1].values,ndmin=1).T
        cyc_current = np.array(current[neg_cycle_no==cn+1].values,ndmin=1).T
        cyc_capacity = -1*(cyc_time*cyc_current)/(3600*active_mass)
        
        ct_name = time_head + "(D" + str(cn+1) + ")"
        all_data[ct_name] = cyc_time
        
        cyc_cap_name =  capacity_head + "(D" + str(cn+1) + ")"
        all_data[cyc_cap_name] = cyc_capacity 
        
        cyc_pot_name = potential_head + "(D" + str(cn+1) + ")"
        all_data[cyc_pot_name] = cyc_pot
    
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
    # print(f"Path length is {len(save_dir)}")
    if len(save_dir) >=200:
        tk.messagebox.showerror(title=None, 
                                message="Your chosen file path is likely too long.\nChose a shorter filename or save your data on a USB drive to shorten the path.")
        raise ValueError('Path lenght is too long.')
    try:
       
        os.mkdir(save_dir)
		
    except FileExistsError:
        pass
    
    filename = os.path.basename(file)
    out_df = pd.DataFrame.from_dict(all_data,orient="columns")
    
    out_df.to_csv(os.path.join(save_dir,"%s%s" % (filename[0:-3],'csv') ), index = True)  
    
    return out_df,filename,save_dir,pos_count,neg_count

def create_cycles_seperate(out_df, save_dir):
    print('Saving individual cycles...')
    cycle_dir = save_dir + "/Individual Cycles"
    try:
        os.mkdir(cycle_dir)
    except FileExistsError:
        pass
    
    for i in range(len(out_df.columns)//6):
        
        
        match_C = '(C' + str(i+1) + ')'
        current_charge_cols = [col for col in out_df.columns if match_C in col]
        match_D = '(D' + str(i+1) + ')'
        current_discharge_cols = [col for col in out_df.columns if match_D in col]
        usecols = current_charge_cols + current_discharge_cols
        Cycle_x = out_df[usecols]
        Cycle_x.to_csv(os.path.join(cycle_dir,"Cycle_%d.csv" % (i+1)), index = True)
        
        if i==0:         
            c_capacity,c_potential,d_capacity,d_potential = cyc.hysteresis_data_from_frame(Cycle_x,str(i+1))
            cyc.plot_hysteresis(c_capacity,c_potential,d_capacity,d_potential,str(i+1),save_dir)
            
    print('Individual cycles saved!')
if __name__ == "__main__":
    
    out_df,file,save_dir,_,_ = create_data_frame()
    

            
            
