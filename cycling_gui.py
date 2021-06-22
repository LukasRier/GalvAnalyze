# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:43:20 2021

@author: lukas
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from clean_data import check_valid_mass
import clean_data as cld
import cycling_plots as cyc
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('CyclingApp')
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
        self.filen_entry.grid(row=2, column=0,columnspan = 25,sticky=tk.W,**options)
        
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
        self.c1var = tk.BooleanVar(value=False)
        self.save_indv_cycles_cb = ttk.Checkbutton(self, 
                        text = "Save individual charge and discharge cycles",
                        variable = self.c1var, onvalue=True, offvalue=False)
        self.save_indv_cycles_cb.grid(column=0,row=5,columnspan=4, sticky=tk.W,**options)
        
        # select whether cycling currents vary in time
        self.c2var = tk.BooleanVar(value=False)
        self.save_indv_cycles_cb = ttk.Checkbutton(self, 
                        text = "Time varying peak current",
                        variable = self.c2var, onvalue=True, offvalue=False)
        self.save_indv_cycles_cb.grid(column=0,row=6, sticky=tk.W,**options)
        
        
        #confirm and run clean data/plots
        self.run_plots_btn = ttk.Button( self, text = "Run Cycling", command=self.runPlotsBtnCallback )
        self.run_plots_btn.grid(column=24,row=6, sticky=tk.E,**options)
        
        
        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)
        self.pack()
    def fileBtnCallback(self):
        self.file = filedialog.askopenfilename(filetypes=[('Text files','*.txt')])
        self.filen_entry.delete(0,len(self.tkFileVar.get()))               
        self.filen_entry.insert(0,self.file)    
    
    def massBtnCallback(self):
        print()
        if not(check_valid_mass(self.tkMassVar.get())):
            tk.messagebox.showerror(title=None, 
                                    message="Enter a valid number!")
            self.mass_entry.delete(0,len(self.tkMassVar.get()))
            self.mass_entry.insert(0,"Enter Mass")
        else:
            self.mass = self.tkMassVar.get()
            print(self.mass)
            
    def runPlotsBtnCallback(self):
        print(self.c2var.get())
        
        out_df,filename,save_dir,pos_count,neg_count = cld.create_data_frame(self.file,self.mass,not(self.c2var.get()))
        
        if self.c1var.get() == True:
            cld.create_cycles_seperate(out_df, save_dir)
    
        
        (coulombic_efficiency, max_charge_cap, 
         max_discharge_cap) = cyc.calculate_max_cap_and_coulombic_eff(out_df,pos_count,neg_count)
    
        cycle_no = cyc.get_cycle_no(pos_count)
    
        # max cap and coulombic efficiency plot
        cyc.plot_max_cap_and_efficiency(cycle_no, max_charge_cap, max_discharge_cap, coulombic_efficiency,save_dir)
    
    
        cyc.save_max_pap_csv(save_dir,cycle_no,max_charge_cap,max_discharge_cap,coulombic_efficiency)

        cyc.plot_caps_vs_potentials(out_df,pos_count,neg_count,save_dir)
        
if __name__ == "__main__":
    app = App()
    CyclingFrame(app)
    app.mainloop()