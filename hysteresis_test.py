# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 21:17:56 2021

@author: Lukas Rier
"""
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
import tkinter as tk
import os

import re

root = tk.Tk()
root.withdraw()

## hysteresis callback start
file = filedialog.askopenfilename(parent=root,
                                  filetypes=[('Text files','*.csv')],
                                  title='Open CSV file for a specific cycle')
filepath = os.path.abspath(file)
pattern = re.compile(r'Cycle_\d+')
fname_match = re.findall(pattern,file)

if len(fname_match) != 1:
    raise ValueError('This file is not named correctly.\n Generate separate cycling files using the GUI')

cycle_no = re.findall(r'Cycle_(\d+).csv',file)[0]
df = pd.read_csv(filepath)
def hysteresis_data_from_frame(df):
    # time_head = "Elapsed time/s "
    potential_head = "Ecell/V "
    capacity_head = "Capacity/mA.h.g^-1 "
    
    c_pot_name = potential_head + "(C" + cycle_no + ")"
    c_cap_name = capacity_head + "(C" + cycle_no + ")"
    
    c_potential = df.loc[:,c_pot_name]
    c_capacity = df.loc[:,c_cap_name]
    
    d_pot_name = potential_head + "(D" + cycle_no + ")"
    d_cap_name = capacity_head + "(D" + cycle_no + ")"
    
    d_potential = df.loc[:,d_pot_name]
    d_capacity = df.loc[:,d_cap_name]
    return c_capacity,c_potential,d_capacity,d_potential
## end of callback, run plot hysteresis from within

# plot hysteresis function receives c/d_potential c/d_capacity, flips d_cap and plots
d_capacity_h = -1*d_capacity + c_capacity[c_capacity.index.get_loc(c_capacity.last_valid_index())]


plt.figure(figsize=(20,10))

plt.subplot(1,2,1)
plt.plot(c_capacity,c_potential,'b')
plt.plot(d_capacity,d_potential,'r')
plt.xlabel("Capacity $\mathrm{mAh g^{-1}}$")
plt.ylabel("Cycle %s : Potential V" % cycle_no)
plt.title('raw')

plt.subplot(1,2,2)
plt.plot(c_capacity,c_potential,'b')
plt.plot(d_capacity_h,d_potential,'r')
plt.xlabel("Capacity $\mathrm{mAh g^{-1}}$")
plt.ylabel("Cycle %s : Potential V" % cycle_no)
plt.title('Hysteresis')

