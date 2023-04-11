# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 20:16:32 2020

@authors: lukas Rier & Rory McNulty
lukasrier@outlook.com
"""
import sys
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# parameters for parquet compression
PARQUET_COMPRESSION: str = "gzip"
PARQUET_ENGINE: str = "fastparquet"


def data_from_file(file=None, active_mass_input=None):
    """
    Reads data from a text file specified by the user and returns the file path, the loaded data, and the active mass.

    Parameters:
    file (str): the file path to be read. If None, a file dialog will be shown to select a file.
    active_mass_input (str): the user input for active mass. If None, a dialog will be shown to prompt the user for input.

    Returns:
    tuple: a tuple containing:
        - str: the file path of the data file
        - pandas.DataFrame: the loaded data
        - float: the active mass in grams
    """
    if file is None:
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
    data = pd.read_csv(file, delimiter='\t' or ',')

    if active_mass_input is None:
        mass_valid = False
    else:
        mass_valid = check_valid_number(active_mass_input)
    while not(mass_valid):
        if not 'root' in locals():
            root = tk.Tk()
            root.lift()
        active_mass_input = simpledialog.askstring(parent=root,
                                                   title="Active Mass",
                                                   prompt="Enter Active Loading (mg):",
                                                   initialvalue=8)
        if active_mass_input is None:
            if 'root' in locals():
                root.destroy()
            msg = "You need an active mass value to proceed."
            raise Exception(msg)

        mass_valid = check_valid_number(active_mass_input)

        if not mass_valid:
            tk.messagebox.showerror(title=None,
                                    message="Enter a valid number!")

    if 'root' in locals():
        root.destroy()

    active_mass = float(active_mass_input) / 1000

    return file, data, active_mass


def check_valid_number(input_str):
    """
    Checks whether a string can be converted to a positive, non-zero number.

    Parameters:
    input_str (str): the input string to be checked.

    Returns:
    bool: True if the input can be converted to a positive, non-zero number, False otherwise.
    """
    try:
        val = float(input_str)
    except ValueError:
        return False
    except TypeError:
        return False
    if val <= 0:
        return False
    else:
        return True


def parse_data(data):
    """
    Parses the loaded data and returns the potential, time, and current.

    Parameters:
    data (pandas.DataFrame): the loaded data to be parsed.

    Returns:
    tuple: a tuple containing:
        - pandas.Series: the potential data
        - pandas.Series: the time data
        - pandas.Series: the current data
    """
    if 'Ecell/V' in data:
        potential = data.loc[:, 'Ecell/V']
    elif 'E /V' in data:
        potential = data.loc[:, 'E /V']
    elif 'Ewe/V' in data:
        potential = data.loc[:, 'Ewe/V']
    elif 'E/V' in data:
        potential = data.loc[:, 'E/V']
    elif 'Voltage/V' in data:
        potential = data.loc[:, 'Voltage/V']
    elif 'Voltage(V)' in data:
        potential = data.loc[:, 'Voltage(V)']
    else:
        potential = 'NaN'
    print(potential)

    if '<I>/mA' in data:
        current = data.loc[:, '<I>/mA']
    elif 'I /mA' in data:
        current = data.loc[:, 'I /mA']
    elif 'I/mA' in data:
        current = data.loc[:, 'I/mA']
    elif 'Current/mA' in data:
        current = data.loc[:, 'Current/mA']
    elif 'Current(A)' in data:
        current = data.loc[:, 'Current(A)']*1000
    else:
        current = 'NaN'
    print(current)

    if 'time/s' in data:
        time = data.loc[:, 'time/s']
    elif 'time /s' in data:
        time = data.loc[:, 'time /s']
    else:
        time = 'NaN'
    print(time)

    return potential, time, current


def const_current_thresh_diagnostic(current, posthresh, negthresh):
    """
    Plots the current data with positive and negative threshold lines.

    Parameters:
    current (pandas.Series): the current data to be plotted.
    posthresh (float): the positive threshold value.
    negthresh (float): the negative threshold value.
    """
    plt.figure()
    ax = plt.subplot(111)
    ax.plot(current, 'k')
    ax.plot(np.arange(1, len(current)+1),
            posthresh * np.ones((len(current))), 'r')
    ax.plot(np.arange(1, len(current)+1),
            negthresh * np.ones((len(current))), 'b')


def variable_current_thresh_diagnostic(current, thresh, in_cycle, absgrad):
    """
    Plot diagnostic graphs for current threshold analysis.

    Parameters:
    current (array-like): An array of current values.
    thresh (float): The current threshold value.
    in_cycle (array-like): Boolean array indicating whether the data point is in a cycle.
    absgrad (array-like): An array of absolute gradient values.

    Returns:
    None
    """
    plt.figure()
    ax = plt.axes()
    ax.plot(current, 'k')
    ax.plot(thresh * np.ones((len(current))), 'r')
    ax.plot(-1 * thresh * np.ones((len(current))), 'b')

    plt.figure()
    ax2 = plt.axes()
    ax2.hist(current, bins=10)

    plt.figure()
    ax3 = plt.axes()
    ax3.plot(absgrad, 'k')
    plt.title('absgrad')
    # ax.plot(in_cycle,'r--')
    ax3.plot(in_cycle * np.sign(current), 'r--')


def check_min_curr_correct(incycle_thresh):
    """
    Validate the current threshold input and return the validated threshold value.

    Parameters:
    incycle_thresh (float): The initial value for the current threshold.

    Returns:
    incycle_thresh (float): The validated current threshold value.
    """
    incycle_thresh_valid = False
    while not(incycle_thresh_valid):
        if not 'root' in locals():
            root = tk.Tk()
            root.lift()
        incycle_thresh_input = simpledialog.askstring(parent=root,
                                                      title="Min current threshold",
                                                      prompt="Desired current threshold (mA):",
                                                      initialvalue=incycle_thresh)

        if incycle_thresh_input is None:
            if 'root' in locals():
                root.destroy()
            msg = "You need a threshold value to proceed."
            raise Exception(msg)

        incycle_thresh_valid = check_valid_number(incycle_thresh_input)

        if not(incycle_thresh_valid):
            tk.messagebox.showerror(title=None,
                                    message="Enter a valid number!")

    if 'root' in locals():
        root.destroy()
    incycle_thresh = float(incycle_thresh_input)

    return incycle_thresh

def current_thresholds(current, rel_cutoff=0.98, is_constant=True):
    """
    Find positive and negative current thresholds based on input current data.

    Parameters:
    current (array-like): An array of current values.
    rel_cutoff (float): A relative cutoff value for finding the current thresholds.
    is_constant (bool): A boolean value indicating whether the current is constant or not.

    Returns:
    is_pos (array-like): Boolean array indicating whether a data point is in a positive cycle.
    is_neg (array-like): Boolean array indicating whether a data point is in a negative cycle.
    """
    if is_constant:
        posthresh = rel_cutoff * np.max(current)
        negthresh = rel_cutoff * np.min(current)
        pos_cycles = current > posthresh
        neg_cycles = -1 * (current < negthresh)
        is_pos = pos_cycles != 0
        is_neg = neg_cycles != 0

        # Diagnostic plots! uncomment if needed
        # const_current_thresh_diagnostic(current,posthresh,negthresh)
    else:
        absgrad = np.abs(find_edges(current))

        incycle_thresh = np.min(np.unique(absgrad[absgrad > 0]))

        incycle_thresh = check_min_curr_correct(incycle_thresh)
        in_cycle = absgrad < incycle_thresh

        # get rid of initial period
        if in_cycle[0] == 1:
            in_cycle[0] = 0
            st = 1
            while in_cycle[st] == 1:
                in_cycle[st] = 0
                st += 1
            print("removed ", st, "points from the beginning")

        # Diagnostic plots! uncomment if needed
        # const_current_thresh_diagnostic(current,1,1)
        # variable_current_thresh_diagnostic(current,0,in_cycle,absgrad)

        signed_in_cycle = in_cycle * np.sign(current)
        is_pos = signed_in_cycle == 1
        is_neg = signed_in_cycle == -1
    return is_pos, is_neg


def find_edges(is_incycle):
    """
    Find the edges in a boolean array.

    Parameters:
    is_incycle (array-like): Boolean array indicating whether a data point is in a cycle.

    Returns:
    edge (array-like): An array of edge values.
    """
    edge = np.convolve(is_incycle, [1, -1], mode='same')
    return edge


def get_cycle_counts(time, is_pos, is_neg):
    """
    Find the number of positive and negative cycles in the input data.

    Parameters:
    time (array-like): An array of time values.
    is_pos (array-like): Boolean array indicating whether a data point is in a positive cycle.
    is_neg (array-like): Boolean array indicating whether a data point is in a negative cycle.

    Returns:
    pos_count (int): The number of positive cycles.
    neg_count (int): The number of negative cycles.
    pos_cycle_no (array-like): An array of positive cycle numbers.
    neg_cycle_no (array-like): An array of negative cycle numbers.
    """
    pos_edge, neg_edge = find_edges(is_pos), find_edges(is_neg)

    pos_cycle_no = np.zeros(time.shape)*np.nan
    pos_count = 0
    neg_cycle_no = np.zeros(time.shape)*np.nan
    neg_count = 0

    for i, _ in enumerate(time):
        if is_pos[i]:
            if pos_edge[i] == 1:
                pos_count += 1
                pos_cycle_no[i-2] = pos_count
            pos_cycle_no[i] = pos_count

        if is_neg[i]:
            if neg_edge[i] == 1:
                neg_count += 1
                neg_cycle_no[i-2] = neg_count
            neg_cycle_no[i] = neg_count

    print("Number of neg cycles = %d \nNumber of pos cycles = %d" %
          (neg_count, pos_count))

    if pos_count > neg_count:
        pos_cycle_no[pos_cycle_no > neg_count] = np.nan
        pos_count = neg_count
    elif pos_count < neg_count:
        neg_cycle_no[neg_cycle_no > pos_count] = np.nan
        neg_count = pos_count

    print("Number of neg cycles = %d \nNumber of pos cycles = %d" % (
        np.nanmax(neg_cycle_no), np.nanmax(pos_cycle_no)))

    return pos_count, neg_count, pos_cycle_no, neg_cycle_no

# Here we need to create the value of capacity
# Capacity = time*current (mAs) / 3600 (mAh) / active mass (g) = mAh g^-1


def create_data_frame(file=None, active_mass=None, is_constant=True, do_parquet=False):
    """
    Creates a Pandas DataFrame containing the cycling data from an input file.

    Parameters:
    file (str): The name of the input file containing the cycling data.
    active_mass (float): The active mass of the electrode material in grams.
    is_constant (bool): A boolean indicating whether or not the cycling current is constant.
    do_parquet (bool): A boolean indicating whether or not to save the output in the Parquet format.

    Returns:
    out_df (pandas.DataFrame): The cycling data as a Pandas DataFrame.
    filename (str): The name of the input file.
    save_dir (str): The path to the directory where the output file(s) will be saved.
    pos_count (int): The number of positive cycles in the input data.
    neg_count (int): The number of negative cycles in the input data.
    """

    file, data, active_mass = data_from_file(file, active_mass)

    (potential,
     time, current) = parse_data(data)

#    grav_capacity = capacity / active_mass

    is_pos, is_neg = current_thresholds(current, 0.98, is_constant)

    # pos_edge,neg_edge = find_edges(is_pos),find_edges(is_neg)

    (pos_count, neg_count,
     pos_cycle_no, neg_cycle_no) = get_cycle_counts(time, is_pos, is_neg)

    all_data = dict()

    time_head = "Elapsed_time/s"
    potential_head = "Ecell/V"
    capacity_head = "Capacity/mA.h.g^-1"
    for cn in range(pos_count):
        exp_time = np.array(time[pos_cycle_no == cn+1].values, ndmin=1).T
        cyc_time = exp_time - exp_time[0]
        cyc_pot = np.array(potential[pos_cycle_no == cn+1].values, ndmin=1).T
        cyc_current = np.array(current[pos_cycle_no == cn+1].values, ndmin=1).T
        cyc_capacity = (cyc_time*cyc_current)/(3600*active_mass)

        ct_name = time_head + "(C" + str(cn+1) + ")"
        all_data[ct_name] = cyc_time

        cyc_cap_name = capacity_head + "(C" + str(cn+1) + ")"
        all_data[cyc_cap_name] = cyc_capacity

        cyc_pot_name = potential_head + "(C" + str(cn+1) + ")"
        all_data[cyc_pot_name] = cyc_pot

    for cn in range(neg_count):
        exp_time = np.array(time[neg_cycle_no == cn+1].values, ndmin=1).T
        cyc_time = exp_time - exp_time[0]
        cyc_pot = np.array(potential[neg_cycle_no == cn+1].values, ndmin=1).T
        cyc_current = np.array(current[neg_cycle_no == cn+1].values, ndmin=1).T
        cyc_capacity = -1*(cyc_time*cyc_current)/(3600*active_mass)

        ct_name = time_head + "(D" + str(cn+1) + ")"
        all_data[ct_name] = cyc_time

        cyc_cap_name = capacity_head + "(D" + str(cn+1) + ")"
        all_data[cyc_cap_name] = cyc_capacity

        cyc_pot_name = potential_head + "(D" + str(cn+1) + ")"
        all_data[cyc_pot_name] = cyc_pot

    length = np.array([])

    for col in all_data:
        arr = all_data[col]
        sh = np.shape(arr)
        length = np.append(length, sh[0])

    max_length = np.max(length)

    for i, col in enumerate(all_data):
        buffer = np.zeros(int(round(max_length)))*np.nan
        orig_len = np.max(np.shape(all_data[col]))
        buffer[0:orig_len] = all_data[col]
        all_data[col] = buffer

    save_dir = file[0:-4] + "_OUTPUTS"
    # print(f"Path length is {len(save_dir)}")
    if len(save_dir) >= 200:
        tk.messagebox.showerror(title=None,
                                message="Your chosen file path is likely too long.\nChose a shorter filename or save your data on a USB drive to shorten the path.")
        raise ValueError('Path lenght is too long.')
    try:

        os.mkdir(save_dir)

    except FileExistsError:
        pass

    filename = os.path.basename(file)
    out_df = pd.DataFrame.from_dict(all_data, orient="columns")

    if do_parquet:
        out_df.to_parquet(os.path.join(save_dir, "%s%s" % (filename[0:-3], 'parquet')),
                          index=True,
                          engine=PARQUET_ENGINE,
                          compression=PARQUET_COMPRESSION)
    else:
        out_df.to_csv(os.path.join(save_dir, "%s%s" % (filename[0:-3], 'csv')),
                      index=True)
    return out_df, filename, save_dir, pos_count, neg_count


def create_cycles_separate(out_df, save_dir, do_parquet=False):
    """
    Splits the input DataFrame into separate DataFrames, one for each cycle, and saves each cycle as a separate file.

    Parameters:
    out_df (pandas.DataFrame): The input DataFrame containing the cycling data.
    save_dir (str): The path to the directory where the output file(s) will be saved.
    do_parquet (bool): A boolean indicating whether or not to save the output in the Parquet format.

    Returns:
    None
    """
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
        current_discharge_cols = [
            col for col in out_df.columns if match_D in col]
        usecols = current_charge_cols + current_discharge_cols
        Cycle_x = out_df[usecols]

        if do_parquet:
            Cycle_x.to_parquet(os.path.join(cycle_dir, "Cycle_%d.parquet" % (i+1)),
                               index=True,
                               engine=PARQUET_ENGINE,
                               compression=PARQUET_COMPRESSION)
            print(f"Cycle {i+1} saved as .parquet!")
        else:
            Cycle_x.to_csv(os.path.join(cycle_dir, "Cycle_%d.csv" % (i+1)),
                           index=True)
            print(f"Cycle {i+1} saved as .csv!")


if __name__ == "__main__":
    out_df, file, save_dir, _, _ = create_data_frame()
