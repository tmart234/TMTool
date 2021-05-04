# this form helps modelers describe data flows within the model
# this script takes all model's "flows" as input, dynamically creates an input form
# based on the number of flows, & then the modeler sets CIA + severity metrics for each flow
# MODELING TIP: a model should always contain flows describing how data-at-rest gets stored/extracted 
#  from a system (don't just capture data-in-motion). Since threats are generated based on flows,
#  CIA is also infered from flows
# TODO: also have notes and justification as text input
# TODO: since severity is a threat prop, for (some) threats we could store it in the template and chose worst case
#        PyTM uses severity as a threat property: https://github.com/izar/pytm/blob/master/docs/threats.md

import tkinter as tk
from tkinter import ttk
# override the basic Tk widgets
from tkinter import *
from ttkthemes import ThemedStyle
from . import tooltip

class AssetsWindow(ttk.Frame):
    def __init__(self, master, flows, *args, **kwargs):
        self.master = master
        self.flows = flows
        self.Assets = dict()

        self.master.configure(background='#404040')
        self.master.title('ASSET FORM')
        style = ThemedStyle(self.master)
        style.set_theme("equilux")
        ttk.Frame.__init__(self, master, *args, **kwargs)
        self.label_frame = ttk.Frame(self.master)
        self.label_frame.grid()
        self.label_list = []

        self.label_list.append(ttk.Label(self.label_frame, text="List of Assets"))
        self.label_list.append(ttk.Button(self.label_frame, text="Add new Asset", command=self.add_new_data))
        for ndex, i in enumerate(self.label_list):
            i.grid(row=ndex)

    # open a user input form for adding an asset that will be shown on the root screen
    def add_new_data(self):
        self.new_f = tk.Tk()
        self.new_f.configure(background='#404040')
        self.new_f.title('NEW ASSET')
        style = ThemedStyle(self.new_f)
        style.set_theme("equilux")

        a_B1 = ttk.Button(self.new_f, text="Add Asset", command=self.quit_new_asset)
        _lb1 = Listbox(self.new_f, selectmode='multiple', background='#404040', foreground='#FFFFFF')
        _lb2 = Listbox(self.new_f, selectmode='multiple', background='#404040', foreground='#FFFFFF')
        _t1 = ttk.Label(self.new_f, text="Severity Impact:", font=(None, 12, 'bold'))
        _t2 = ttk.Label(self.new_f, text="Flows Impacted:",  font=(None, 12, 'bold'))

        safe_data=("No Injuries", "Light Injuries", "Severe Injuries", "Life-threatening")
        fin_data=("No Financial Impact", "Low Impact", "Substantial Loss", "Devastating")
        op_data=("No Effect", "Minor Disruption", "Moderate Disruption", "Major Disruption", "Fails Saftey Reqs")
        priv_data=("No Effect", "Low", "Medium", "High")
        asset_knowledge=("Public","Restricted","Sensitive","Critical")
        asset_weights=("Low","Medium","High")
        asset_loss_factors = ("IP", "Personal Identifiers", "Health Data (PHI)", "Strategic Info", "Reputation", "Monetary", "Regulations", "Forensic/Logging" )

        _t3 = ttk.Label(self.new_f, text="Asset Safty Impact")
        _t4 = ttk.Label(self.new_f, text="Asset Financial Impact")
        _t5 = ttk.Label(self.new_f, text="Asset Operational Impact")
        _t6 = ttk.Label(self.new_f, text="Asset Privacy Impact")

        _t7 = ttk.Label(self.new_f, text="Short Title:", font=(None, 12, 'bold'))
        _e1 = ttk.Entry(self.new_f)
        _t8 = ttk.Label(self.new_f, text="Description:")
        _e2 = ttk.Entry(self.new_f)

        _t9 = ttk.Label(self.new_f, text="Required Knowledge:",  font=(None, 12, 'bold'))
        _t10 = ttk.Label(self.new_f, text="Asset Valued Weight:",  font=(None, 12, 'bold'))
        _t11 = ttk.Label(self.new_f, text="Cost/Loss Item:",  font=(None, 12, 'bold'))

        _cb1 = ttk.Combobox(self.new_f, values=safe_data)
        _cb2 = ttk.Combobox(self.new_f, values=fin_data)
        _cb3 = ttk.Combobox(self.new_f, values=op_data)
        _cb4 = ttk.Combobox(self.new_f, values=priv_data)
        _cb5 = ttk.Combobox(self.new_f, values=asset_knowledge)
        _cb6 = ttk.Combobox(self.new_f, values=asset_weights)
        _cb1.current(0)
        _cb2.current(0)
        _cb3.current(0)
        _cb4.current(0)
        _cb5.current(0)
        _cb6.current(0)
        # get list of model flow names
        flo_names = list()
        for i in range(0, len(self.flows)):
            flo_names.append(str(dict(list(self.flows.values())[i]).get('Name')))
        # fill Listboxes    
        for item in flo_names:
            _lb1.insert('end', item)
        for item in asset_loss_factors:
            _lb2.insert('end', item)
        # keep LB selection when clicking elsewhere
        _lb1.configure(exportselection=False)
        _lb2.configure(exportselection=False)
        
        self.new_f.columnconfigure(0, weight=1)
        self.new_f.columnconfigure(1, weight=1)

        _t7.grid(row=0, column= 0, sticky='nsew')
        _e1.grid(row=1, column= 0, sticky='nsew')
        _t8.grid(row=2, column= 0, sticky='nsew')
        _e2.grid(row=3, column= 0, sticky='nsew')
        # Listboxes
        _t2.grid(row=4, column= 0, sticky='nsew')
        _lb1.grid(row=5, rowspan=5, column= 0, sticky='nsew')
        _t11.grid(row=10, column= 0, sticky='nsew')
        _lb2.grid(row=11, rowspan=2, column= 0, sticky='nsew')
        # comboboxes
        _t1.grid(row=0, column= 1, sticky='nsew')
        _t3.grid(row=1, column= 1, sticky='nsew')
        _cb1.grid(row=2, column= 1, sticky='nsew')
        _t4.grid(row=3, column= 1, sticky='nsew')
        _cb2.grid(row=4, column= 1, sticky='nsew')
        _t5.grid(row=5, column= 1, sticky='nsew')
        _cb3.grid(row=6, column= 1, sticky='nsew')
        _t6.grid(row=7, column= 1, sticky='nsew')
        _cb4.grid(row=8, column= 1, sticky='nsew')
        _t9.grid(row=9, column= 1, sticky='nsew')
        _cb5.grid(row=10, column= 1, sticky='nsew')
        _t10.grid(row=11, column= 1, sticky='sew')
        _cb6.grid(row=12, column= 1, rowspan=1, sticky='new')

        a_B1.grid(row=13, column= 0, columnspan=2, sticky='nsew')
        # hover-over tips
        tooltip.CreateToolTip(_t1, \
            "Select all severity Impact Levels which apply")
        tooltip.CreateToolTip(_t2, \
            "Select all model flows which interact with the asset")
        tooltip.CreateToolTip(_t9, \
            "Availability of the asset's information")
        tooltip.CreateToolTip(_t10, \
            "Importance of this asset compared to other assets")
        tooltip.CreateToolTip(_t11, \
            "Consequences of a compromised asset")
        self.new_f.mainloop()

    ## quit the "new asset" window
    def quit_new_asset(self):
        if not len(self.Assets):
            a_len = 1
        else:
            a_len = len(self.Assets)+1
        # add asset to dict
        self.Assets[a_len]='new'+str(a_len)
        # add label
        self.label_list.insert(1, ttk.Label(self.label_frame, text=self.Assets.get(a_len)))
        for widget in self.label_frame.children.values():
            widget.grid_forget() 
        for ndex, i in enumerate(self.label_list):
            i.grid(row=ndex)
        # resize root
        x = 200
        y = (a_len*35+25)
        self.master.geometry(str(x) + "x" + str(y))

        self.new_f.destroy()


def main(flows):
    root = tk.Tk()
    app = AssetsWindow(root, flows)
    app.mainloop()

if __name__ == '__main__':
   main()