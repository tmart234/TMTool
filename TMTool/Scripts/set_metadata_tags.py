# this script will set a model's metadata (such as risk level and compliance)
# as a set of tags in a threat model's Note entries
from tkinter import ttk
from tkinter.ttk import *
import tkinter as tk
from ttkthemes import ThemedStyle
from tkinter import filedialog
from tkinter.ttk import Combobox
from lxml import etree
import datetime
from . import tooltip as TP

def get_boxes_and_destroy():
    global notes_dict
    notes_dict = dict.fromkeys(['CR','IR', 'AR', 'TD','CWE','CAPEC'])
    notes_dict['CR'] = cb1.get() 
    notes_dict['IR'] = cb2.get() 
    notes_dict['AR'] = cb3.get() 
    notes_dict['TD'] = cb4.get()
    notes_dict['CWE'] = c1.get()
    notes_dict['CAPEC'] = c2.get()
    #print(notes_dict)
    save_to_xml()
    quit()

def delete_note(root, _id):
    for notes in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Notes'):
        for note in notes.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Note'):
            for id in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Id'):
                if int(id.text) == int(_id):
                    root[2].remove(note)
                    print('removed note: ' + str(_id))
    return

def save_to_xml():
    _root = tk.Tk()
    # hide window
    _root.withdraw()

    # get CSV
    try:
        model_path = filedialog.askopenfilename(parent=_root, filetypes=[("model file", "*.tm7")])
        tree = etree.parse(model_path)
        _root = tree.getroot()
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    if not model_path:
        print('Must choose file path, quitting... ')
        quit()

    id = None
    msgs = dict()
    
    # find all note elements
    for notes in _root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Notes'):
        for note in notes.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Note'):
            for id in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Id'):
                _id = id.text
            for message in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Message'):
                _message = str(message.text)
            msgs[_id] = _message

    if not msgs:
        id = 1
    else:
        k = list(msgs.keys())
        id = int(k[-1]) + 1
        # overwrite if tag exists
        for key,value in msgs.items():
            if 'METADATA:' in value:
                print("Warning: model already contains METADATA note")
                print("Overwriting note..")
                id = int(key)
                delete_note(_root, id)

    new_note = etree.Element("Note")
    added = etree.SubElement(new_note, 'AddedBy')
    added.text = "TMTool"
    date = etree.SubElement(new_note, 'Date')
    d = str(datetime.datetime.now().strftime('%Y-%m-%d'))
    t = str(datetime.datetime.now().time())
    # fix to get it into required format for MS tmt
    date.text = str(d + 'T' + t + '0-07:00')
    _id = etree.SubElement(new_note, 'Id')
    _id.text = str(id)
    message = etree.SubElement(new_note, 'Message')
    message.text = str('METADATA: '+ str(notes_dict))
    # insert in Notes in last position
    _root[2].insert((id-1), new_note)
    print('added note: ' + str(notes_dict))
    print('ID: ' + str(id))

    tree.write(model_path)
    return

def main():
    root = tk.Tk()
    root.configure(background='#404040')
    root.title('Model Metadata')
    root.geometry("400x350+10+10")
    style = ThemedStyle(root)
    style.set_theme("equilux")

    global c1
    global c2
    c1 = tk.IntVar()    
    c2 = tk.IntVar()      
    # Create text widget and specify size. 
    T1 = ttk.Label(root, text='Compliance Standards:', font=(None, 13, 'bold'))
    T2 = ttk.Label(root, text='Security Requirements:', font=(None, 13, 'bold'))
    T3 = ttk.Label(root, text='Confidentiality Requirement')
    T4 = ttk.Label(root, text='Integrity Requirement')
    T5 = ttk.Label(root, text='Availability Requirement')
    T6 = ttk.Label(root, text='Target Distribution')
    R1= Button(root, text="Done", command=get_boxes_and_destroy)

    T1.place(x=25, y=15)
    C1 = tk.Checkbutton(root, text = "CWE", variable = c1, background='#404040', fg='#ffffff', selectcolor='#000000')
    C2 = tk.Checkbutton(root, text = "CAPEC", variable = c2, background='#404040', fg='#ffffff', selectcolor='#000000')
    C1.place(x=25, y=40)
    C2.place(x=105, y=40)

    T2.place(x=25, y=75)
    T3.place(x=25, y=100)
    data=("Not Defined", "Low", "Medium", "High")
    global cb1
    cb1=ttk.Combobox(root, values=data)
    cb1.current(0)
    cb1.place(x=25, y=125)

    T4.place(x=25, y=165)
    data=("Not Defined", "Low", "Medium", "High")
    global cb2
    cb2=ttk.Combobox(root, values=data)
    cb2.current(0)
    cb2.place(x=25, y=190)

    T5.place(x=25, y=240)
    data=("Not Defined", "Low", "Medium", "High")
    global cb3
    cb3=ttk.Combobox(root, values=data)
    cb3.current(0)
    cb3.place(x=25, y=265)

    T6.place(x=200, y=240)
    data=("None","Low", "Medium", "High")
    global cb4
    cb4=ttk.Combobox(root, values=data)
    cb4.current(0)
    cb4.place(x=200, y=265)

    R1.place(x=150,y=318)

    # have-over definitions
    TP.CreateToolTip(T1, \
        "Select the desired compliance standards. Compliance tag URLs will show up in the generated report"
        " after fixing the hyperlinks with TMTool")
    TP.CreateToolTip(T2, \
        "Determine the specific security requirements for confidentiality, integrity and availability. "
        "This allows the final score to be tuned according to the users' environment and is similar to the users' risk threshold")
    TP.CreateToolTip(T6, \
        "Determine the proportion of vulnerable systems within the model. "
        "Ex: a threat ID affects only Windows, but half the environment systems run MacOS. Can be over ridden in analysis mode.")

    root.mainloop()
    return

if __name__ == '__main__':
    main()