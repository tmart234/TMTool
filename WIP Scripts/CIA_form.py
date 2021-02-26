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
from tkinter.scrolledtext import ScrolledText

def get_boxes_and_destroy():
    quit()


def main(flows):
    root = tk.Tk()
    root.configure(background='#404040')
    root.title('CIA FORM')
    f_len = len(flows)
    x = 850
    y = ((f_len+1)*35*2+15)
    root.geometry(str(x) + "x" + str(y))
    style = ThemedStyle(root)
    style.set_theme("equilux")

    # configure columns
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=1)
    root.columnconfigure(5, weight=1)

    # Headers
    _l1 = ttk.Label(root, text='Flow Name', font=(None, 13, 'bold'))
    _l2 = ttk.Label(root, text='Assets', font=(None, 13, 'bold'))
    _l3 = ttk.Label(root, text='Confidentiality', font=(None, 13, 'bold'))
    _l4 = ttk.Label(root, text='Integrity', font=(None, 13, 'bold'))
    _l5 = ttk.Label(root, text='Availibility', font=(None, 13, 'bold'))
    _l6 = ttk.Label(root, text='Justification', font=(None, 13, 'bold'))
    _r1 = ttk.Button(root, text="Done", command=get_boxes_and_destroy)
    _l1.grid(row=0, column=0, sticky=W+E)
    _l2.grid(row=0, column=1, sticky=W+E)
    _l3.grid(row=0, column=2, sticky=W+E)
    _l4.grid(row=0, column=3, sticky=W+E)
    _l5.grid(row=0, column=4, sticky=W+E)
    _l6.grid(row=0, column=5, sticky=W+E)


    data=("Not Defined", "Low", "Medium", "High")
    sev=("Not Defined", "Low", "Medium Low", "Medium", "Medium High", "High")
    for i in range(0, len(flows)):
        l1 = ttk.Label(root, text=dict(list(flows.values())[i]).get('Name'), font=(None, 13, 'bold'))
        e1 = Text(root,height=4,width=20, background='#404040', foreground='#FFFFFF')
        e2 = Text(root,height=4,width=20, background='#404040', foreground='#FFFFFF')
        cb1 = ttk.Combobox(root, values=data)
        cb2 = ttk.Combobox(root, values=data)
        cb3 = ttk.Combobox(root, values=data)
        cb1b = ttk.Combobox(root, values=sev)
        cb2b = ttk.Combobox(root, values=sev)
        cb3b = ttk.Combobox(root, values=sev)
        cb1.current(0)
        cb2.current(0)
        cb3.current(0)
        cb1b.current(0)
        cb2b.current(0)
        cb3b.current(0)
        l1.grid(row=((i+1)*2), column=0, sticky=W+E)
        e1.grid(row=((i+1)*2), column=1, rowspan=2,  sticky='ewns')
        e2.grid(row=((i+1)*2), column=5, rowspan=2, sticky='ewns')
        cb1.grid(row=((i+1)*2), column=2, sticky=W+E)
        cb2.grid(row=((i+1)*2), column=3, sticky=W+E)
        cb3.grid(row=((i+1)*2), column=4, sticky=W+E)
        _l7 = ttk.Label(root, text='Severity', font=(None, 9, 'italic'))
        _l7.grid(row=(((i+1)*2)+1), column=0, sticky=E)
        cb1b.grid(row=(((i+1)*2)+1), column=2, sticky=W+E)
        cb2b.grid(row=(((i+1)*2)+1), column=3, sticky=W+E)
        cb3b.grid(row=(((i+1)*2)+1), column=4, sticky=W+E)
        
    _r1.grid(row=(((len(flows)+1)*2)+2), columnspan=3, column=2, sticky='ewns')
    root.mainloop()

if __name__ == '__main__':
   main()