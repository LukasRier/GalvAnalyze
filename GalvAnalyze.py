# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:43:20 2021

@authors: lukas Rier  & Rory McNulty
lukasrier@outlook.com
"""
import re
import os
import logging
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from clean_data import check_valid_number
import clean_data as cld
import cycling_plots as cyc



class App(tk.Tk):
    """Main application window that contains all other widgets."""

    def __init__(self):
        """Initialize the App class."""
        super().__init__()
        self.title('GalvAnalyze')
        iconfile = 'logos\\GalvAnalyzeIcon.ico'
        # include icon if included
        if os.path.isfile(iconfile):
            self.iconbitmap(iconfile)
        self.call('tk', 'scaling', 1.5)
        self.geometry('1100x250')
        self.resizable(False, False)


class CyclingFrame(ttk.Frame):
    """Frame for cycling plot and data analysis options."""

    def __init__(self, container):
        """Initialize the CyclingFrame class.

        Args:
            container (object): Parent container for the frame.
        """
        super().__init__(container)

        options = {'padx': 5,
                   'pady': 5}

        # File selection
        self.file = "No File Selected"

        self.tk_file_var = tk.StringVar(self, value=self.file)
        self.file_btn = ttk.Button(
            self, text="Load file", command=self.file_button_callback)

        self.filen_entry = ttk.Entry(
            self, textvariable=self.tk_file_var, width=100)

        # mass selection
        self.mass = "Enter Mass"
        self.tk_mass_var = tk.StringVar(self, value=self.mass)
        self.mass_entry_lbl = ttk.Label(self, text="Active Mass:")

        self.mass_unit_lbl = ttk.Label(self, text="mg")

        self.mass_entry = ttk.Entry(self, textvariable=self.tk_mass_var)

        self.cnfrm_mass_btn = ttk.Button(
            self, text="Confirm Mass", command=self.mass_button_callback)

        # select whether to save individual charge discharge cycles
        self.separate_cycles_checkbox_var = tk.BooleanVar(value=False)
        self.save_indv_cycles_cb = ttk.Checkbutton(self,
                                                   text="Save separate charge-\ndischarge pairs to file.",
                                                   variable=self.separate_cycles_checkbox_var,
                                                   onvalue=True,
                                                   offvalue=False)

        # select whether cycling currents vary in time
        self.current_varies_checkbox_var = tk.BooleanVar(value=False)
        self.current_varies_cb = ttk.Checkbutton(self,
                                                   text="Applied current varies",
                                                   variable=self.current_varies_checkbox_var,
                                                   onvalue=True,
                                                   offvalue=False)

        # select whether the first cycle is a charge (true) or discharge (false)
        self.first_cyc_charge_checkbox_var = tk.BooleanVar(value=True)
        self.charge_first_cb = ttk.Checkbutton(self,
                                               text="First cycle is charge",
                                               variable=self.first_cyc_charge_checkbox_var,
                                               onvalue=True,
                                               offvalue=False)

        # select whether to use parquet file format
        self.do_parquet = tk.BooleanVar(value=False)
        self.do_parquet_cb = ttk.Checkbutton(self,
                                             text="Use Parquet files",
                                             variable=self.do_parquet,
                                             onvalue=True,
                                             offvalue=False)

        # confirm and run clean data/plots
        self.run_plots_btn = ttk.Button(
            self, text="Run Cycling", command=self.run_plots_button_callback)

        # hysteresis plots
        self.do_hysteresis_btn = ttk.Button(self, text="Get Hysteresis Plot",
                                            command=self.run_hysteresis)

        # Set layout of GUI elements
        self.file_btn.grid(row=0, column=7, sticky=tk.NW, **options)
        self.filen_entry.grid(
            row=0, column=0, columnspan=6, sticky=tk.W, **options)
        self.mass_entry_lbl.grid(row=3, column=0, sticky=tk.W, **options)
        self.mass_entry.grid(row=4, column=0, sticky=tk.W, **options)
        self.mass_unit_lbl.grid(row=4, column=1, sticky=tk.W)
        self.cnfrm_mass_btn.grid(row=4, column=2, sticky=tk.W, **options)
        self.save_indv_cycles_cb.grid(row=5, column=0, sticky=tk.W, **options)
        self.current_varies_cb.grid(row=6, column=0, sticky=tk.W, **options)
        self.charge_first_cb.grid(row=7, column=0, sticky=tk.W, **options)
        self.do_parquet_cb.grid(row=6, column=4, sticky=tk.W, **options)
        self.run_plots_btn.grid(row=6, column=5, sticky=tk.E, **options)
        self.do_hysteresis_btn.grid(row=7, column=5, sticky=tk.E, **options)

        # add padding to the frame and show it
        self.grid(padx=0, pady=0)
        self.pack()

    def file_button_callback(self):
        """
        Callback function for the 'Select File' button.

        Allows the user to select a text file and sets the selected file path to the 'file' attribute of the instance.
        Updates the text in the 'filen_entry' Entry widget with the selected file path.

        Returns:
        None
        """

        self.file = filedialog.askopenfilename(
            filetypes=[('Text files', '*.txt')])
        self.filen_entry.delete(0, len(self.tk_file_var.get()))
        self.filen_entry.insert(0, self.file)

        # configure log file name and formatting
        log_fname = self.file[:-4] + '.log'
        logging.basicConfig(filename=log_fname, level=logging.WARNING,
                            filemode='w', format='%(asctime)s %(message)s')
        logging.warning('File selected!')
        plt.ion()

    def mass_button_callback(self):
        """
        Callback function for the 'Confirm Mass' button.

        Validates the mass value entered by the user.
        If the mass is invalid, shows an error message and resets the mass value in the Entry widget to 'Enter Mass'.
        If the mass is valid, sets the mass value to the 'mass' attribute of the instance.

        Returns:
        None
        """
        logging.warning('Confirming active mass value...')
        if not check_valid_number(self.tk_mass_var.get()):
            logging.warning('Active mass value not valid! Asking for another...')
            tk.messagebox.showerror(title=None,
                                    message="Enter a valid number!")
            self.mass_entry.delete(0, len(self.tk_mass_var.get()))
            self.mass_entry.insert(0, "Enter Mass")
        else:
            self.mass = self.tk_mass_var.get()
            print(self.mass)
            logging.warning(f'Active mass value valid ({self.mass} mg)')


    def run_plots_button_callback(self):
        """
        Callback function for the 'Run Plots' button.

        Runs the necessary functions to create and save various plots based on the selected file and mass values.
        Depending on the status of the 'current_varies_checkbox_var' and 'separate_cycles_checkbox_var' attributes,
        the function creates data frames, calculates charge and discharge capacities, cycles and saves data, and
        creates plots of max capacity, coulombic efficiency, capacity vs. potential, and hysteresis.

        Returns:
        None
        """
        print(self.current_varies_checkbox_var.get())
        if self.current_varies_checkbox_var.get():
            logging.warning('Creating dataframe. Assuming applied current varies')
        else:
            logging.warning('Creating dataframe. Assuming applied current is constant')

        if self.do_parquet.get():
            logging.warning('Using Parquet format instead of CSV!')
        out_df, _, save_dir, pos_count, neg_count = cld.create_data_frame(self.file,
                                                                          self.mass,
                                                                          not(self.current_varies_checkbox_var.get()),
                                                                          self.do_parquet.get())
        
        if self.separate_cycles_checkbox_var.get() is True:
            logging.warning('Saving individual cycles...')
            cld.create_cycles_separate(out_df, save_dir, self.do_parquet.get())

        (coulombic_efficiency, max_charge_cap,
         max_discharge_cap) = cyc.calculate_max_cap_and_coulombic_eff(out_df, pos_count, neg_count)

        cycle_no = cyc.get_cycle_no(pos_count)

        # max cap and coulombic efficiency plot
        logging.warning('Plotting maximum capacity and efficiency...')
        cyc.plot_max_cap_and_efficiency(
            cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency, save_dir)
        
        logging.warning('Saving table of max capacities...')
        cyc.save_max_cap_csv(save_dir, cycle_no, max_charge_cap,
                             max_discharge_cap, coulombic_efficiency)
        
        logging.warning('Creating capacity vs potential plot...')
        cyc.plot_caps_vs_potentials(out_df, pos_count, neg_count, save_dir)

        # plot first cycle hysteresis
        logging.warning('Creating hysteresis plot for cycle 1...')
        match_c = '(C1)'
        current_charge_cols = [col for col in out_df.columns if match_c in col]
        match_d = '(D1)'
        current_discharge_cols = [
            col for col in out_df.columns if match_d in col]
        usecols = current_charge_cols + current_discharge_cols
        cycle_1 = out_df[usecols]
        c_capacity, c_potential, d_capacity, d_potential = cyc.hysteresis_data_from_frame(
            cycle_1, str(1))
        charge_first = self.first_cyc_charge_checkbox_var.get()
        if charge_first is True:
            logging.warning('Assuming first cycle is charge')
        else:
            logging.warning('Assuming first cycle is discharge')
        cyc.plot_hysteresis(c_capacity, c_potential, d_capacity,
                            d_potential, str(1), save_dir, charge_first)
                
    def run_hysteresis(self):
        """Open a file dialog to select a specific cycle file, load the file into a pandas dataframe, and plot the hysteresis
        curve of the cycle.

        Raises:
        ValueError: If the selected file is not a valid cycle file generated using the GUI.

        Returns:
        None
        """
        if self.do_parquet.get():
            filetype = ('Parquet files', '*.parquet')
        else:
            filetype = ('CSV files', '*.csv')
        logging.warning('Choosing file for hysteresis plots')
        cycle_file = filedialog.askopenfilename(filetypes=[filetype],
                                                title='Open file for a specific cycle')
        cyc_filepath = os.path.abspath(cycle_file)

        pattern = re.compile(r'Cycle_\d+')
        fname_match = re.findall(pattern, cycle_file)

        if len(fname_match) != 1:
            msg = 'This is not a valid file.\n Generate separate cycling files using the GUI'
            tk.messagebox.showerror(title='File error',
                                    message=msg)
            logging.error(msg)
            raise ValueError(msg)

        if self.do_parquet.get():
            cycle_df = pd.read_parquet(cyc_filepath)
            hyst_cycle_no = re.findall(r'Cycle_(\d+).parquet', cycle_file)[0]
        else:
            cycle_df = pd.read_csv(cyc_filepath)
            hyst_cycle_no = re.findall(r'Cycle_(\d+).csv', cycle_file)[0]
        logging.warning(f'Generating hysteresis plot for cycle {hyst_cycle_no}.')
        cyc_save_dir = os.path.dirname(cyc_filepath)
        c_capacity, c_potential, d_capacity, d_potential = cyc.hysteresis_data_from_frame(
            cycle_df, hyst_cycle_no)
        charge_first = self.first_cyc_charge_checkbox_var.get()
        cyc.plot_hysteresis(c_capacity, c_potential, d_capacity,
                            d_potential, hyst_cycle_no, cyc_save_dir, charge_first)


if __name__ == "__main__":
    app = App()
    CyclingFrame(app)
    app.mainloop()
