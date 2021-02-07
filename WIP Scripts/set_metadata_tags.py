# this script will set a model's metadata (such as risk level and compliance)
# as a set of tags in a threat model's Note entries
# work in progress!!
# TODO: export selected tags to a model note entry (write to the XML file)

from tkinter import *
from tkinter.ttk import Combobox

root=Tk()
root.configure(background='#243447')
                
v1 = IntVar()
v2 = IntVar()
t1 = StringVar()
t2 = StringVar()
t3 = StringVar()
t4 = StringVar()
t5 = StringVar()
# Create text widget and specify size. 
T1 = Label(root, textvariable=t1, bg="#243447", fg='#ffffff')
T2 = Label(root, textvariable=t2, bg="#243447", fg='#ffffff')
T3 = Label(root, textvariable=t3, bg="#243447", fg='#ffffff')
T4 = Label(root, textvariable=t4, bg="#243447", fg='#ffffff')
T5 = Label(root, textvariable=t5, bg="#243447", fg='#ffffff')

t1.set('Compliance Standards:')
T1.place(x=25, y=25)
C1 = Checkbutton(root, text = "CWE", variable = v1, background="#243447",fg='#ffffff', selectcolor='#000000')
C2 = Checkbutton(root, text = "CAPEC", variable = v2, background="#243447",fg='#ffffff', selectcolor='#000000')
C1.place(x=25, y=50)
C2.place(x=105, y=50)

t2.set('Security Requirements')
T2.place(x=25, y=125)
t3.set('Confidentiality')
T3.place(x=25, y=150)
data=("Low", "Medium", "High")
cb1=Combobox(root, values=data)
cb1.place(x=25, y=175)

t4.set('Integrity')
T4.place(x=25, y=200)
data=("Low", "Medium", "High")
cb2=Combobox(root, values=data)
cb2.place(x=25, y=225)

t5.set('Availability')
T5.place(x=25, y=250)
data=("Low", "Medium", "High")
cb3=Combobox(root, values=data)
cb3.place(x=25, y=275)

root.title('Model Metadata')
root.geometry("400x300+10+10")
root.mainloop()


# yes/no button
# v0=IntVar()
# v0.set(1)
# r1=Radiobutton(window, text="Yes", variable=v0,value=1)
# r2=Radiobutton(window, text="No", variable=v0,value=2)
# r1.place(x=100,y=50)
# r2.place(x=180, y=50)