# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 21:53:53 2020

@authors: Lukas Rier & Rory McNulty
lukasrier@outlook.com
"""

import clean_data as cld
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def calculate_max_cap_and_coulombic_eff(out_df, pos_count, neg_count):    
    charge_cols = [col for col in out_df.columns if 'Capacity/mA.h.g^-1 (C' in col]
    max_charge_cap = np.zeros(pos_count)
    for i,col in enumerate(charge_cols):
        max_charge_cap[i]=np.max(out_df[col])
        
    discharge_cols =  [col for col in out_df.columns if 'Capacity/mA.h.g^-1 (D' in col]
    max_discharge_cap = np.zeros(neg_count)
    for i,col in enumerate(discharge_cols):
        max_discharge_cap[i]=np.max(out_df[col])
    
    if max_discharge_cap[0] > max_charge_cap[0]:
        coulombic_efficiency = 100*max_charge_cap/max_discharge_cap
    elif max_discharge_cap[0] < max_charge_cap[0]:
        coulombic_efficiency = 100*max_discharge_cap/max_charge_cap
    elif max_discharge_cap[0] == max_charge_cap[0]:
        coulombic_efficiency = 100*max_discharge_cap/max_charge_cap
    return coulombic_efficiency, max_charge_cap, max_discharge_cap 

def get_cycle_no(pos_count):    
    cycle_no = np.arange(1,pos_count+1)
    return cycle_no



def plot_max_cap_and_efficiency(cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency,save_dir):
    # max cap and coulombic efficiency plot
    fig,ax = plt.subplots()
    ax.plot(cycle_no, max_discharge_cap, 'x')
    ax.plot(cycle_no, max_charge_cap, 'x')
    ax.legend(["Discharge capacity", "Charge capacity"], loc='lower left')
    ax.set_xlabel("Cycle Number", fontsize=14)
    plt.xticks(fontsize=14)
    ax.set_ylabel("Capacity $\mathrm{mAh g^{-1}}$", fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(bottom=0)
    
    
    ax2=ax.twinx()
    ax2.plot(cycle_no, coulombic_efficiency, 'o')
    ax2.set_ylabel("Coulombic efficiency %", fontsize=14)
    ax2.legend(['Coulombic efficiency'], loc='lower right')
    plt.ylim([0,110])
    plt.yticks(fontsize=14)
    plt.savefig(os.path.join(save_dir,"Cycle no vs. Capacity and Coulombic efficiency.png"))
    
    plt.tight_layout()
    plt.show()
    
    
    
    
    
def save_max_pap_csv(save_dir,cycle_no,max_charge_cap,max_discharge_cap,coulombic_efficiency):   
    max_cap = {'Cycle Number': cycle_no, 
               'Max Charge Capacity mA.h.g^-1': max_charge_cap,
               'Max Discharge Capacity mA.h.g^-1': max_discharge_cap,
               'Coulombic Efficiency' : coulombic_efficiency}
    max_cap_df = pd.DataFrame.from_dict(data=max_cap,orient="columns")
    max_cap_path = os.path.join(save_dir,"Max_capacities_per_cycle.csv")
    # max_cap_path = os.path.join(save_dir,"%s%s" % ('test','_max_capacities_per_cycle.csv'))
    max_cap_df.to_csv(max_cap_path, index = False)   





def plot_caps_vs_potentials(out_df,pos_count,neg_count,save_dir=None):    
    
    charge_cyc_potentials = np.zeros((out_df.shape[0],pos_count))
    charge_cyc_capacities = np.zeros((out_df.shape[0],pos_count))  
    
    for coln in range(pos_count):
        charge_cyc_potentials[:,coln] = out_df["Ecell/V (C%d)" % (coln+1)]
        charge_cyc_capacities[:,coln] = out_df["Capacity/mA.h.g^-1 (C%d)" % (coln+1)]
        
    # plt.figure()
    # plt.plot(charge_cyc_capacities,charge_cyc_potentials, linewidth=0.5)
    # plt.xlabel("Capacity $mAh g^{-1}$", fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.ylabel("Potential / $V$", fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.tight_layout()
    # plt.legend(["Cyc1","Cyc2","Cyc3","Cyc4","Cyc5","Cyc6","Cyc7","Cyc8","Cyc9","Cyc10"])
    # if save_dir != None:
    #    plt.savefig(os.path.join(save_dir,"Charge capacity vs. Potential.png"))
    
    discharge_cyc_potentials = np.zeros((out_df.shape[0],neg_count))
    discharge_cyc_capacities = np.zeros((out_df.shape[0],neg_count))
    
    for coln in range(neg_count):
        discharge_cyc_potentials[:,coln] = out_df["Ecell/V (D%d)" % (coln+1)]
        discharge_cyc_capacities[:,coln] = out_df["Capacity/mA.h.g^-1 (D%d)" % (coln+1)]
    
    # plt.figure()
    # plt.plot(discharge_cyc_capacities[:,coln],discharge_cyc_potentials[:,coln], linewidth=0.5)
    # plt.xlabel("Capacity $mAh g^{-1}$", fontsize=14)
    # plt.xticks(fontsize=14)
    # plt.ylabel("Potential / $V$", fontsize=14)
    # plt.yticks(fontsize=14)
    # plt.tight_layout()
    # plt.legend(["Cyc1","Cyc2","Cyc3","Cyc4","Cyc5","Cyc6","Cyc7","Cyc8","Cyc9","Cyc10"])
    # if save_dir != None:
    #     plt.savefig(os.path.join(save_dir,"Disharge capacity vs. Potential.png"))
    
    
    plt.figure()
    for coln in range(neg_count):  
        plt.plot(discharge_cyc_capacities[:,coln],discharge_cyc_potentials[:,coln],
                 linewidth=0.5)
        plt.plot(charge_cyc_capacities[:,coln],charge_cyc_potentials[:,coln],
                 linewidth=0.5)
    plt.xlabel("Capacity $\mathrm{mAh g^{-1}}$", fontsize=14)
    plt.xticks(fontsize=14)
    plt.ylabel("Potential / $\mathrm{V}$", fontsize=14)
    plt.yticks(fontsize=14)
    plt.legend(["D1","C1","D2","C2","D3","C3","D4","C4","D5","C5"], bbox_to_anchor=(0.5, -0.2), ncol=10)
    plt.tight_layout()
    if save_dir != None:
        plt.savefig(os.path.join(save_dir,"Capacity vs. Potential (all cycles).png"))
    plt.show()
    
    return charge_cyc_potentials,charge_cyc_capacities,discharge_cyc_potentials,discharge_cyc_capacities





if __name__ == "__main__":
    
    out_df,filename,save_dir,pos_count,neg_count = cld.create_data_frame()
    
    cld.create_cycles_seperate(out_df, save_dir)
    
        
    (coulombic_efficiency, max_charge_cap, 
     max_discharge_cap) = calculate_max_cap_and_coulombic_eff(out_df,pos_count,neg_count)

    cycle_no = get_cycle_no(pos_count)
    
    # max cap and coulombic efficiency plot
    plot_max_cap_and_efficiency(cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency,save_dir)
    
    
    save_max_pap_csv(save_dir,cycle_no,max_charge_cap,max_discharge_cap,coulombic_efficiency)

    plot_caps_vs_potentials(out_df,pos_count,neg_count,save_dir)
