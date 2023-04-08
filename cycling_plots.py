# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 21:53:53 2020

@authors: Lukas Rier & Rory McNulty
lukasrier@outlook.com
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import clean_data as cld

colors = ['#a6cee3', '#1f78b4', '#b2df8a', '#33a02c', '#fb9a99',
          '#e31a1c', '#fdbf6f', '#ff7f00', '#cab2d6', '#6a3d9a']


def calculate_max_cap_and_coulombic_eff(out_df, pos_count, neg_count):
    """
    This function calculates the maximum charge and discharge capacities, as well as the coulombic efficiency, from a DataFrame.

    Args:
    - out_df: a pandas DataFrame containing the data from the battery cycling experiment
    - pos_count: an integer representing the number of cycles in the charge direction
    - neg_count: an integer representing the number of cycles in the discharge direction

    Returns:
    - coulombic_efficiency: a numpy array containing the coulombic efficiency for each cycle
    - max_charge_cap: a numpy array containing the maximum charge capacity for each cycle
    - max_discharge_cap: a numpy array containing the maximum discharge capacity for each cycle
    """
    charge_cols = [
        col for col in out_df.columns if 'Capacity/mA.h.g^-1(C' in col]
    max_charge_cap = np.zeros(pos_count)
    for i, col in enumerate(charge_cols):
        max_charge_cap[i] = np.max(out_df[col])

    discharge_cols = [
        col for col in out_df.columns if 'Capacity/mA.h.g^-1(D' in col]
    max_discharge_cap = np.zeros(neg_count)
    for i, col in enumerate(discharge_cols):
        max_discharge_cap[i] = np.max(out_df[col])

    if max_discharge_cap[0] > max_charge_cap[0]:
        coulombic_efficiency = 100*max_charge_cap/max_discharge_cap
    elif max_discharge_cap[0] < max_charge_cap[0]:
        coulombic_efficiency = 100*max_discharge_cap/max_charge_cap
    elif max_discharge_cap[0] == max_charge_cap[0]:
        coulombic_efficiency = 100*max_discharge_cap/max_charge_cap
    return coulombic_efficiency, max_charge_cap, max_discharge_cap


def get_cycle_no(pos_count):
    """
    This function returns an array of cycle numbers.
    
    Args:
    - pos_count: an integer representing the number of cycles in the charge direction
    
    Returns:
    - cycle_no: a numpy array containing the cycle numbers starting at 1
    """
    cycle_no = np.arange(1, pos_count+1)
    return cycle_no


def plot_max_cap_and_efficiency(cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency, save_dir):
    """
    This function plots the maximum charge and discharge capacities, as well as the coulombic efficiency, as a function of cycle number.
    
    Args:
    - cycle_no: a numpy array containing the cycle numbers
    - max_charge_cap: a numpy array containing the maximum charge capacity for each cycle
    - max_discharge_cap: a numpy array containing the maximum discharge capacity for each cycle
    - coulombic_efficiency: a numpy array containing the coulombic efficiency for each cycle
    - save_dir: a string representing the directory where the plot should be saved (if None, the plot is not saved)
    """
    plt.figure(figsize=(6.5, 5))
    ax = plt.axes()
    ax.plot(cycle_no, max_discharge_cap, 'x')
    ax.plot(cycle_no, max_charge_cap, 'x')
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.035,
                    box.width, box.height * 0.975])
    ax.legend(["Discharge capacity", "Charge capacity"], loc='lower right',
              bbox_to_anchor=(0.5, 1.01), ncol=1)
    ax.set_xlabel("Cycle Number", fontsize=14)
    plt.xticks(fontsize=14)
    ax.set_ylabel("Capacity / $\mathrm{mAh}$ $\mathrm{g^{-1}}$", fontsize=14)
    plt.yticks(fontsize=14)
    plt.ylim(bottom=0)

    ax2 = ax.twinx()
    ax2.plot(cycle_no, coulombic_efficiency, '^')
    ax2.set_ylabel("Coulombic efficiency / %", fontsize=14)
    ax2.set_position([box.x0, box.y0 + box.height * 0.035,
                     box.width, box.height * 0.975])
    ax2.legend(['Coulombic efficiency'], loc='lower left',
               bbox_to_anchor=(0.5, 1.01), ncol=1)
    plt.ylim([0, 110])
    plt.yticks(fontsize=14)
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(
        save_dir, "Cycle no vs. Capacity and Coulombic efficiency.png"))


def save_max_cap_csv(save_dir, cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency):
    """
    Save the maximum charge and discharge capacities, and coulombic efficiency for each cycle in a csv file.

    Parameters:
    save_dir (str): Directory to save the csv file.
    cycle_no (list): List of cycle numbers.
    max_charge_cap (list): List of maximum charge capacities for each cycle.
    max_discharge_cap (list): List of maximum discharge capacities for each cycle.
    coulombic_efficiency (list): List of coulombic efficiencies for each cycle.

    Returns:
    None
    """
    max_cap = {'Cycle Number': cycle_no,
               'Max Charge Capacity mA.h.g^-1': max_charge_cap,
               'Max Discharge Capacity mA.h.g^-1': max_discharge_cap,
               'Coulombic Efficiency': coulombic_efficiency}
    max_cap_df = pd.DataFrame.from_dict(data=max_cap, orient="columns")
    max_cap_path = os.path.join(save_dir, "Max_capacities_per_cycle.csv")
    max_cap_df.to_csv(max_cap_path, index=False)


def plot_caps_vs_potentials(out_df, pos_count, neg_count, save_dir=None):
    """
    Plot the capacity vs potential for each cycle and save the plot as a png file.

    Parameters:
    out_df (DataFrame): Dataframe containing the electrochemical cycling data.
    pos_count (int): Number of positive cycles.
    neg_count (int): Number of negative cycles.
    save_dir (str): Directory to save the plot as a png file.

    Returns:
    charge_cyc_potentials (ndarray): 2D numpy array containing the potential values for each positive cycle.
    charge_cyc_capacities (ndarray): 2D numpy array containing the capacity values for each positive cycle.
    discharge_cyc_potentials (ndarray): 2D numpy array containing the potential values for each negative cycle.
    discharge_cyc_capacities (ndarray): 2D numpy array containing the capacity values for each negative cycle.
    """
    charge_cyc_potentials = np.zeros((out_df.shape[0], pos_count))
    charge_cyc_capacities = np.zeros((out_df.shape[0], pos_count))

    for coln in range(pos_count):
        charge_cyc_potentials[:, coln] = out_df["Ecell/V(C%d)" % (coln+1)]
        charge_cyc_capacities[:,
                              coln] = out_df["Capacity/mA.h.g^-1(C%d)" % (coln+1)]

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

    discharge_cyc_potentials = np.zeros((out_df.shape[0], neg_count))
    discharge_cyc_capacities = np.zeros((out_df.shape[0], neg_count))

    for coln in range(neg_count):
        discharge_cyc_potentials[:, coln] = out_df["Ecell/V(D%d)" % (coln+1)]
        discharge_cyc_capacities[:,
                                 coln] = out_df["Capacity/mA.h.g^-1(D%d)" % (coln+1)]

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

    plt.figure(figsize=(6, 5))
    for coln in range(neg_count):
        plt.plot(discharge_cyc_capacities[:, coln], discharge_cyc_potentials[:, coln],
                 linewidth=1, color=colors[coln % 10])
        plt.plot(charge_cyc_capacities[:, coln], charge_cyc_potentials[:, coln],
                 linewidth=1, color=colors[coln % 10])
    plt.xlabel("Capacity / $\mathrm{mAh}$ $\mathrm{g^{-1}}$", fontsize=14)
    plt.xticks(fontsize=14)
    plt.ylabel("Potential / $\mathrm{V}$", fontsize=14)
    plt.yticks(fontsize=14)
    ax = plt.gca()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.035,
                    box.width, box.height * 0.975])
    plt.legend(["D1", "C1", "D2", "C2", "D3", "C3", "D4", "C4", "D5", "C5"], loc='lower center',
               bbox_to_anchor=(0.5, 1.01), ncol=5)
    plt.tight_layout()
    plt.show()
    if save_dir != None:
        plt.savefig(os.path.join(
            save_dir, "Capacity vs. Potential (all cycles).png"))

    return charge_cyc_potentials, charge_cyc_capacities, discharge_cyc_potentials, discharge_cyc_capacities


def plot_hysteresis(c_capacity, c_potential, d_capacity, d_potential, cycle_no, save_dir=None, charge_first=True):
    """
    Plots the hysteresis of the charge and discharge curves for a given cycle number.

    Args:
        c_capacity (pd.Series): The capacity data for the charge curve.
        c_potential (pd.Series): The potential data for the charge curve.
        d_capacity (pd.Series): The capacity data for the discharge curve.
        d_potential (pd.Series): The potential data for the discharge curve.
        cycle_no (int): The cycle number to plot.
        save_dir (str, optional): The directory to save the plot and CSV file to. Defaults to None.
        charge_first (bool, optional): Whether the charge curve comes first. Defaults to True.

    Returns:
        None
    """
    plt.figure(figsize=(6, 5))
    ax = plt.axes()
    if charge_first:
        d_capacity_h = -1*d_capacity + \
            c_capacity[c_capacity.index.get_loc(c_capacity.last_valid_index())]
        ax.plot(c_capacity, c_potential, 'k')
        ax.plot(d_capacity_h, d_potential, 'r')
    else:
        c_capacity_h = -1*c_capacity + \
            d_capacity[d_capacity.index.get_loc(d_capacity.last_valid_index())]
        ax.plot(c_capacity_h, c_potential, 'k')
        ax.plot(d_capacity, d_potential, 'r')

    plt.xlabel("Capacity / $\mathrm{mAh}$ $\mathrm{g^{-1}}$", fontsize=14)
    plt.ylabel(f"Cycle {cycle_no} : Potential / V", fontsize=14)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    box = ax.get_position()
    ax.set_position([box.x0, box.y0 + box.height * 0.035,
                    box.width, box.height * 0.975])
    plt.legend(["Charge", "Discharge"], loc='lower center',
               bbox_to_anchor=(0.5, 1.01), ncol=1)
    plt.tight_layout()
    plt.show()

    if save_dir != None:
        plt.savefig(os.path.join(save_dir, f"Cycle {cycle_no} Hysteresis.png"))

        if charge_first:
            hysteresis_df = dict(zip(["Ecell/V (C raw)",
                                      "Capacity/mA.h.g^-1 (C raw)",
                                      "Ecell/V (D raw)",
                                      "Capacity/mA.h.g^-1 (D raw)",
                                      "Capacity/mA.h.g^-1 (D hysteresis)"
                                      ], (c_potential, c_capacity,
                                          d_potential, d_capacity,
                                          d_capacity_h)))
        else:
            hysteresis_df = dict(zip(["Ecell/V (C raw)",
                                      "Capacity/mA.h.g^-1 (C hysteresis)",
                                      "Ecell/V (D raw)",
                                      "Capacity/mA.h.g^-1 (C raw)",
                                      "Capacity/mA.h.g^-1 (D raw)"
                                      ], (c_potential, c_capacity_h,
                                          d_potential, c_capacity,
                                          d_capacity)))

        hysteresis_df = pd.DataFrame.from_dict(hysteresis_df, orient="columns")
        hysteresis_df.to_csv(os.path.join(
            save_dir, f"Cycle {cycle_no} Hysteresis.csv"), index=True)


def hysteresis_data_from_frame(cycle_df, cycle_no):
    """
    Extracts the potential and capacity data for a given cycle number from a DataFrame.

    Args:
        cycle_df (pd.DataFrame): The DataFrame containing the data.
        cycle_no (int): The cycle number to extract.

    Returns:
        pd.Series: The capacity data for the charge curve.
        pd.Series: The potential data for the charge curve.
        pd.Series: The capacity data for the discharge curve.
        pd.Series: The potential data for the discharge curve.
    """
    potential_head = "Ecell/V"
    capacity_head = "Capacity/mA.h.g^-1"

    c_pot_name = potential_head + "(C" + cycle_no + ")"
    c_cap_name = capacity_head + "(C" + cycle_no + ")"

    c_potential = cycle_df.loc[:, c_pot_name]
    c_capacity = cycle_df.loc[:, c_cap_name]

    d_pot_name = potential_head + "(D" + cycle_no + ")"
    d_cap_name = capacity_head + "(D" + cycle_no + ")"

    d_potential = cycle_df.loc[:, d_pot_name]
    d_capacity = cycle_df.loc[:, d_cap_name]
    return c_capacity, c_potential, d_capacity, d_potential


if __name__ == "__main__":
    out_df, filename, save_dir, pos_count, neg_count = cld.create_data_frame()
    cld.create_cycles_separate(out_df, save_dir)

    (coulombic_efficiency,
     max_charge_cap,
     max_discharge_cap) = calculate_max_cap_and_coulombic_eff(out_df, pos_count, neg_count)

    cycle_no = get_cycle_no(pos_count)

    # max cap and coulombic efficiency plot
    plot_max_cap_and_efficiency(
        cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency, save_dir)
    save_max_cap_csv(save_dir, cycle_no, max_charge_cap,
                     max_discharge_cap, coulombic_efficiency)
    plot_caps_vs_potentials(out_df, pos_count, neg_count, save_dir)
