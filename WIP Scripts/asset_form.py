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

def get_boxes_and_destroy():
    quit()

def quit(_root):
    _root.destroy()

def new_asset(_root, _flows):
    new_f = tk.Tk()
    new_f.configure(background='#404040')
    new_f.title('NEW ASSET')
    style = ThemedStyle(new_f)
    style.set_theme("equilux")

    a_B1 = ttk.Button(new_f, text="Add", command=lambda: quit(new_f))
    _lb1 = Listbox(new_f, selectmode='multiple', background='#404040', foreground='#FFFFFF')
    _t1 = ttk.Label(new_f, text="Asset Severity:")
    _t2 = ttk.Label(new_f, text="Flows Impacted:")
    safe_data=("No Injuries", "Light Injuries", "Severe Injuries", "Life-threatening")
    fin_data=("No Financial Impact", "Low Impact", "Substantial Loss", "Devastating")
    op_data=("No Effect", "Minor Disruption", "Moderate Disruption", "Major Disruption", "Fails Saftey Reqs")
    priv_data=("No Effect", "Low", "Medium", "High")
    _t3 = ttk.Label(new_f, text="Asset Safty Impact")
    _t4 = ttk.Label(new_f, text="Asset Financial Impact")
    _t5 = ttk.Label(new_f, text="Asset Operational Impact")
    _t6 = ttk.Label(new_f, text="Asset Privacy Impact")
    _t7 = ttk.Label(new_f, text="Asset Name:")
    _e1 = ttk.Entry(new_f)
    _cb1 = ttk.Combobox(new_f, values=safe_data)
    _cb2 = ttk.Combobox(new_f, values=fin_data)
    _cb3 = ttk.Combobox(new_f, values=op_data)
    _cb4 = ttk.Combobox(new_f, values=priv_data)

    # get list of model flow names
    flo_names = list()
    for i in range(0, len(_flows)):
        flo_names.append(str(dict(list(_flows.values())[i]).get('Name')))
    # fill Listbox    
    for item in flo_names:
        _lb1.insert('end', item)
    
    new_f.rowconfigure(0, weight=1)
    new_f.rowconfigure(1, weight=1)
    new_f.columnconfigure(0, weight=1)
    new_f.columnconfigure(1, weight=1)

    _t7.grid(row=0, column= 0, sticky='nsew')
    _e1.grid(row=1, column= 0, sticky='nsew')
    _t2.grid(row=2, column= 0, sticky='nsew')
    _lb1.grid(row=3, rowspan=6, column= 0, sticky='nsew')
    _t1.grid(row=0, column= 1, sticky='nsew')
    _t3.grid(row=1, column= 1, sticky='nsew')
    _cb1.grid(row=2, column= 1, sticky='nsew')
    _t4.grid(row=3, column= 1, sticky='nsew')
    _cb2.grid(row=4, column= 1, sticky='nsew')
    _t5.grid(row=5, column= 1, sticky='nsew')
    _cb3.grid(row=6, column= 1, sticky='nsew')
    _t6.grid(row=7, column= 1, sticky='nsew')
    _cb4.grid(row=8, column= 1, sticky='nsew')
    a_B1.grid(row=9, column= 0, columnspan=2, sticky='nsew')
    new_f.mainloop()
    # reset root geometry
    if len(Assets) is None:
        _len = 1
    else:
        _len = len(Assets)+1
    # add to Assets
    Assets[_len+1] = 'new'
    x = 200
    y = (_len*35)
    _root.geometry(str(x) + "x" + str(y))
    new_f.destroy()
    return


def main(flows):
    global Assets
    Assets = dict()
    root = tk.Tk()
    root.configure(background='#404040')
    root.title('ASSET FORM')
    style = ThemedStyle(root)
    style.set_theme("equilux")
    
    root.rowconfigure(0, weight=1)

    B1 = ttk.Button(text="Add Asset", command=lambda: new_asset(root, flows))
    B1.grid(row=0, column= 0, sticky='nsew')
    root.mainloop()

if __name__ == '__main__':
   main()