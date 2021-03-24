# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 20:43:20 2021

@author: lukas
"""
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from clean_data import check_valid_mass
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('CyclingApp')
        self.geometry('1000x300')
        self.resizable(True, False)
        
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
        
        #select
        
        # add padding to the frame and show it
        self.grid(padx=10, pady=10, sticky=tk.NSEW)
        
    def fileBtnCallback(self):
        self.file = filedialog.askopenfilename(filetypes=[('Text files','*.txt')])
        self.filen_entry.delete(0,len(self.tkFileVar.get()))               
        self.filen_entry.insert(0,self.file)    
    
    def massBtnCallback(self):
        
        if not(check_valid_mass(self.tkMassVar.get())):
            tk.messagebox.showerror(title=None, 
                                    message="Enter a valid number!")
            self.mass_entry.delete(0,len(self.tkMassVar.get()))
            self.mass_entry.insert(0,"Enter Mass")
        else:
            self.mass = self.tkMassVar.get()
            print(self.mass)
        
if __name__ == "__main__":
    app = App()
    CyclingFrame(app)
    app.mainloop()