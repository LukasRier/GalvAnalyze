# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 21:53:53 2020

@author: Lukas Rier
lukasrier@outlook.com
"""

import clean_data as cld
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

out_df,filename,save_dir,pos_count,neg_count = cld.create_data_frame()


charge_cols = [col for col in out_df.columns if 'Capacity/mA.h.g^-1 (C' in col]
max_charge_cap = np.zeros(pos_count)
for i,col in enumerate(charge_cols):
    max_charge_cap[i]=np.max(out_df[col])
    
discharge_cols =  [col for col in out_df.columns if 'Capacity/mA.h.g^-1 (D' in col]
max_discharge_cap = np.zeros(neg_count)
for i,col in enumerate(discharge_cols):
    max_discharge_cap[i]=np.max(out_df[col])
    
cycle_no = np.arange(1,pos_count+1)

plt.figure()
plt.plot(cycle_no, max_discharge_cap, 'x')
plt.plot(cycle_no, max_charge_cap, 'x')
plt.legend(["Discharge capacity", "Charge capacity"])
plt.xlabel("Cycle Number", fontsize=14)
plt.xticks(fontsize=14)
plt.ylabel("Capacity $mAh g^{-1}$", fontsize=14)
plt.yticks(fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(save_dir,"Cycle no vs. Capacity.png"))
plt.show()

max_cap = {'Cycle Number': cycle_no, 
           'Max Charge Capacity mA.h.g^-1': max_charge_cap,
           'Max Discharge Capacity mA.h.g^-1': max_discharge_cap}
max_cap_df = pd.DataFrame.from_dict(data=max_cap,orient="columns")
max_cap_path = os.path.join(save_dir,"%s%s" % (filename[0:-4],'_max_capacities_per_cycle.csv'))
max_cap_df.to_csv(max_cap_path, index = False)

plt.figure()
charge_cyc_potentials = np.zeros((out_df.shape[0],pos_count))
charge_cyc_capacities = np.zeros((out_df.shape[0],pos_count))
for coln in range(pos_count):
    charge_cyc_potentials[:,coln] = out_df["Ecell/V (C%d)" % (coln+1)]
    charge_cyc_capacities[:,coln] = out_df["Capacity/mA.h.g^-1 (C%d)" % (coln+1)]
    plt.plot(charge_cyc_capacities[:,coln],charge_cyc_potentials[:,coln], linewidth=0.5)
    plt.xlabel("Capacity $mAh g^{-1}$", fontsize=14)
    plt.xticks(fontsize=14)
    plt.ylabel("Potential / $V$", fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
plt.legend(["Cyc1","Cyc2","Cyc3","Cyc4","Cyc5","Cyc6","Cyc7","Cyc8","Cyc9","Cyc10"])
plt.savefig(os.path.join(save_dir,"Charge capacity vs. Potential.png"))

plt.figure()
discharge_cyc_potentials = np.zeros((out_df.shape[0],neg_count))
discharge_cyc_capacities = np.zeros((out_df.shape[0],neg_count))
for coln in range(neg_count):
    discharge_cyc_potentials[:,coln] = out_df["Ecell/V (D%d)" % (coln+1)]
    discharge_cyc_capacities[:,coln] = out_df["Capacity/mA.h.g^-1 (D%d)" % (coln+1)]
    plt.plot(discharge_cyc_capacities[:,coln],discharge_cyc_potentials[:,coln], linewidth=0.5)
    plt.xlabel("Capacity $mAh g^{-1}$", fontsize=14)
    plt.xticks(fontsize=14)
    plt.ylabel("Potential / $V$", fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.legend(["Cyc1","Cyc2","Cyc3","Cyc4","Cyc5","Cyc6","Cyc7","Cyc8","Cyc9","Cyc10"])
plt.savefig(os.path.join(save_dir,"Disharge capacity vs. Potential.png"))

plt.figure()
discharge_cyc_potentials = np.zeros((out_df.shape[0],neg_count))
discharge_cyc_capacities = np.zeros((out_df.shape[0],neg_count))
for coln in range(neg_count):
    discharge_cyc_potentials[:,coln] = out_df["Ecell/V (D%d)" % (coln+1)]
    discharge_cyc_capacities[:,coln] = out_df["Capacity/mA.h.g^-1 (D%d)" % (coln+1)]
    plt.plot(discharge_cyc_capacities[:,coln],discharge_cyc_potentials[:,coln],
             linewidth=0.5)
    plt.plot(charge_cyc_capacities[:,coln],charge_cyc_potentials[:,coln],
             linewidth=0.5)
    plt.xlabel("Capacity $mAh g^{-1}$", fontsize=14)
    plt.xticks(fontsize=14)
    plt.ylabel("Potential / $V$", fontsize=14)
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.legend(["Discharge1","Charge1","Discharge2","Charge2","Discharge3","Charge3"
                ,"Discharge4","Charge4","Discharge5","Charge5"])
plt.savefig(os.path.join(save_dir,"Capacity vs. Potential (all cycles).png"))
