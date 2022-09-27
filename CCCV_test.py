# -*- coding: utf-8 -*-
"""
Created on Mon Jun 20 15:56:45 2022

@author: lukas
"""

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from clean_data import check_valid_mass
import clean_data as cld
import cycling_plots as cyc
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

testfile = filedialog.askopenfilename(filetypes=[('CSV files','*.csv')],
                                                title='Open CSV file for a specific cycle')
test_filepath = os.path.abspath(testfile)

print(test_filepath)

df = pd.read_csv(test_filepath)

potential, time, current = cld.parse_data(df)

plt.figure()
plt.plot(time,potential)
plt.title('Potential')
plt.draw()

plt.figure()
plt.plot(time,current)
plt.title('Current')

pos_current = np.array(current)
neg_current = np.array(current)
pos_current[pos_current < 0] = 0
neg_current[neg_current > 0] = 0

pos_edges = cld.find_edges(pos_current)
neg_edges = cld.find_edges(neg_current)

plt.figure()
plt.plot(time,pos_current,'*-')
plt.plot(time,pos_edges,'*-')
#cycle starts


plt.figure()
plt.plot(time,neg_current,'*-')
plt.plot(time,neg_edges,'*-')

# Charge cycles 
pos_edges_h = pos_edges[pos_edges>0]
plt.figure()
plt.hist(pos_edges_h, 10)
