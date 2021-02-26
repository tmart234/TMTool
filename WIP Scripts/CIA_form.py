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

def main(flows):
    root = tk.Tk()
    root.configure(background='#404040')
    root.title('CIA FORM')
    f_len = len(flows)
    x = 600
    y = (f_len+1)*35
    root.geometry(str(x) + "x" + str(y))
    style = ThemedStyle(root)
    style.set_theme("equilux")

    # configure columns
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    # Headers
    _l1 = ttk.Label(root, text='Name', font=(None, 13, 'bold'))
    _l2 = ttk.Label(root, text='Assets', font=(None, 13, 'bold'))
    _l3 = ttk.Label(root, text='Confidentiality', font=(None, 13, 'bold'))
    _l4 = ttk.Label(root, text='Severity', font=(None, 13, 'bold'))
    _l1.grid(row=0, column=0, sticky=W+E)
    _l2.grid(row=0, column=1, sticky=W+E)
    _l3.grid(row=0, column=2, sticky=W+E)
    _l4.grid(row=0, column=3, sticky=W+E)

    data=("Not Defined", "Low", "Medium", "High")
    sev=("Not Defined", "Low", "Medium Low", "Medium", "Medium High", "High")
    for i in range(0, len(flows)):
        l1 = ttk.Label(root, text=dict(list(flows.values())[i]).get('Name'))
        e1 = ttk.Entry(root)
        cb1 = ttk.Combobox(root, values=data)
        cb2 = ttk.Combobox(root, values=sev)
        cb1.current(0)
        cb2.current(0)
        l1.grid(row=i+1, column=0, sticky=W+E)
        e1.grid(row=i+1, column=1, sticky=W+E)
        cb1.grid(row=i+1, column=2, sticky=W+E)
        cb2.grid(row=i+1, column=3, sticky=W+E)
        
    root.mainloop()

if __name__ == '__main__':
   main()