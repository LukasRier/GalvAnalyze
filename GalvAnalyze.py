# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:43:20 2021

@authors: lukas Rier  & Rory McNulty
lukasrier@outlook.com
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from clean_data import check_valid_number
import clean_data as cld
import cycling_plots as cyc
import pandas as pd
import re
import os

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('GalvAnalyze')
        
        iconfile = 'logos\\GalvAnalyzeIcon.ico'
        # include icon if included 
        if os.path.isfile(iconfile):
            self.iconbitmap(iconfile)
            
        self.geometry('1000x300')
        self.resizable(False, False)
        
class CyclingFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)
        
        options = {'padx': 5,
                   'pady': 5}
        
        #File selection
        self.file = "No File Selected"
        
        self.tkFileVar = tk.StringVar(self, value=self.file)
        self.file_btn = ttk.Button( self, text = "Load file", command=self.fileBtnCallback )
        self.file_btn.grid(column=0,row=0, sticky=tk.NW,**options)

        self.filen_entry = ttk.Entry(self, textvariable=self.tkFileVar,width=95)
        self.filen_entry.grid(row=2, column=0,columnspan = 6,sticky=tk.W,**options)
        
        #mass selection
        self.mass = "Enter Mass"
        self.tkMassVar = tk.StringVar(self, value=self.mass)
        self.mass_entry_lbl = ttk.Label(self,text="Active Mass:")
        self.mass_entry_lbl.grid(row=3, column=0,sticky=tk.W,**options)
        
        self.mass_unit_lbl = ttk.Label(self,text="mg")
        self.mass_unit_lbl.grid(row=4, column=1,sticky=tk.W,**options)
        
        self.mass_entry = ttk.Entry(self, textvariable=self.tkMassVar)
        self.mass_entry.grid(row = 4, column=0,sticky=tk.W,**options)
        
        self.cnfrm_mass_btn = ttk.Button( self, text = "Confirm Mass", command=self.massBtnCallback )
        self.cnfrm_mass_btn.grid(column=2,row=4, sticky=tk.W,**options)
        
        # select whether to save individual charge discharge cycles
        self.separate_cycles_checkbox_var = tk.BooleanVar(value=False)
        self.save_indv_cycles_cb = ttk.Checkbutton(self, 
                        text = "Separate charge-discharge pairs to .csv",
                        variable = self.separate_cycles_checkbox_var, onvalue=True, offvalue=False)
        self.save_indv_cycles_cb.grid(column=0,row=5,columnspan=4, sticky=tk.W,**options)
        
        # select whether cycling currents vary in time
        self.current_varies_checkbox_var = tk.BooleanVar(value=False)
        self.save_indv_cycles_cb = ttk.Checkbutton(self, 
                        text = "Applied current varies",
                        variable = self.current_varies_checkbox_var, onvalue=True, offvalue=False)
        self.save_indv_cycles_cb.grid(column=0,row=6, sticky=tk.W,**options)
        
        # select whether the first cycle is a charge (true) or discharge (false)
        self.first_cyc_charge_checkbox_var = tk.BooleanVar(value=True)
        self.charge_first_cb = ttk.Checkbutton(self,
                        text = "First cycle is charge",
                        variable = self.first_cyc_charge_checkbox_var, onvalue=True, offvalue=False)
        self.charge_first_cb.grid(column=0,row=7, sticky=tk.W,**options)
        
        #confirm and run clean data/plots
        self.run_plots_btn = ttk.Button( self, text = "Run Cycling", command=self.runPlotsBtnCallback )
        self.run_plots_btn.grid(column=5,row=6, sticky=tk.W,**options)
        
        #hysteresis plots
        self.do_hysteresis_btn = ttk.Button(self, text = "Get Hysteresis Plot",
                                            command=self.runHysteresis)
        self.do_hysteresis_btn.grid(column=24,row=7,sticky=tk.E,**options)
        
        
        
        # add padding to the frame and show it
        #self.grid(padx=0, pady=0)
        self.pack()
        
        
    def fileBtnCallback(self):
        self.file = filedialog.askopenfilename(filetypes=[('Text files','*.txt')])
        self.filen_entry.delete(0,len(self.tkFileVar.get()))               
        self.filen_entry.insert(0,self.file)    
    
    def massBtnCallback(self):
        print()
        if not(check_valid_number(self.tkMassVar.get())):
            tk.messagebox.showerror(title=None, 
                                    message="Enter a valid number!")
            self.mass_entry.delete(0,len(self.tkMassVar.get()))
            self.mass_entry.insert(0,"Enter Mass")
        else:
            self.mass = self.tkMassVar.get()
            print(self.mass)
            
    def runPlotsBtnCallback(self):
        print(self.current_varies_checkbox_var.get())
        
        out_df,filename,save_dir,pos_count,neg_count = cld.create_data_frame(self.file,self.mass,not(self.current_varies_checkbox_var.get()))
        
        if self.separate_cycles_checkbox_var.get() == True:
            cld.create_cycles_separate(out_df, save_dir)
    
        
        (coulombic_efficiency, max_charge_cap, 
         max_discharge_cap) = cyc.calculate_max_cap_and_coulombic_eff(out_df,pos_count,neg_count)
    
        cycle_no = cyc.get_cycle_no(pos_count)
    
        # max cap and coulombic efficiency plot
        cyc.plot_max_cap_and_efficiency(cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency,save_dir)
    
    
        cyc.save_max_cap_csv(save_dir,cycle_no,max_charge_cap,max_discharge_cap,coulombic_efficiency)

        cyc.plot_caps_vs_potentials(out_df,pos_count,neg_count,save_dir)
        
        #plot first cycle hysteresis
        match_C = '(C1)'
        current_charge_cols = [col for col in out_df.columns if match_C in col]
        match_D = '(D1)'
        current_discharge_cols = [col for col in out_df.columns if match_D in col]
        usecols = current_charge_cols + current_discharge_cols
        Cycle_1 = out_df[usecols]
        c_capacity,c_potential,d_capacity,d_potential = cyc.hysteresis_data_from_frame(Cycle_1,str(1))
        charge_first = self.first_cyc_charge_checkbox_var.get()
        cyc.plot_hysteresis(c_capacity,c_potential,d_capacity,d_potential,str(1),save_dir,charge_first)
        
    def runHysteresis(self):
        cycle_file = filedialog.askopenfilename(filetypes=[('CSV files','*.csv')],
                                                title='Open CSV file for a specific cycle')
        cyc_filepath = os.path.abspath(cycle_file)
        
        pattern = re.compile(r'Cycle_\d+')
        fname_match = re.findall(pattern,cycle_file)

        if len(fname_match) != 1:
            msg = 'This is not a valid file.\n Generate separate cycling files using the GUI'
            tk.messagebox.showerror(title='File error', 
                                    message=msg)
            raise ValueError(msg)
        
        hyst_cycle_no = re.findall(r'Cycle_(\d+).csv',cycle_file)[0]
        cycle_df = pd.read_csv(cyc_filepath)
        cyc_save_dir = os.path.dirname(cyc_filepath) 
        c_capacity,c_potential,d_capacity,d_potential = cyc.hysteresis_data_from_frame(cycle_df,hyst_cycle_no)
        charge_first = self.first_cyc_charge_checkbox_var.get()
        cyc.plot_hysteresis(c_capacity,c_potential,d_capacity,d_potential,hyst_cycle_no,cyc_save_dir,charge_first)
        
if __name__ == "__main__":
    app = App()
    CyclingFrame(app)
    app.mainloop()