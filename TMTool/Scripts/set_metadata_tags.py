# this script will set a model's metadata (such as risk level and compliance)
# as a set of tags in a threat model's Note entries

from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from lxml import etree
import datetime

def check_cb():
    if not cb1.get():
        return False
    elif not cb2.get():
        return False
    elif not cb3.get():
        return False
    elif not cb4.get():
        return False
    else:
        return True

def get_boxes_and_destroy():
    global notes_dict
    notes_dict = dict.fromkeys(['CR','IR', 'AR', 'TD','CWE','CAPEC'])
    if check_cb():
        notes_dict['CR'] = cb1.get() 
        notes_dict['IR'] = cb2.get() 
        notes_dict['AR'] = cb3.get() 
        notes_dict['TD'] = cb4.get()
        notes_dict['CWE'] = v1.get()
        notes_dict['CAPEC'] = v2.get()
        #print(notes_dict)
        root.destroy()
        return
    else:
        print('must choose values for comboboxes')
        return

def save_to_xml():
    _root = Tk()
    # hide root window
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
    ids = []
    
    # find next _id
    for notes in _root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Notes'):
        for note in notes.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Note'):
            for _id in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Id'):
                # should be an int
                ids.append(int(_id.text))
    
    id = ids[-1] + 1

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
    message.text = str('METADATA: '+ notes_dict)
    # insert in Notes in last position
    _root[2].insert((id-1), new_note)
    print('added note: ' + str(notes_dict))
    print('ID: ' + str(id))

    tree.write(model_path)


def main():
    global root
    root = Tk()
    root.configure(background='#243447')

    global v1
    global v2                
    v1 = IntVar()
    v2 = IntVar()
    t1 = StringVar()
    t2 = StringVar()
    t3 = StringVar()
    t4 = StringVar()
    t5 = StringVar()
    t6 = StringVar()
    # Create text widget and specify size. 
    T1 = Label(root, textvariable=t1, bg="#243447", fg='#ffffff')
    T2 = Label(root, textvariable=t2, bg="#243447", fg='#ffffff')
    T3 = Label(root, textvariable=t3, bg="#243447", fg='#ffffff')
    T4 = Label(root, textvariable=t4, bg="#243447", fg='#ffffff')
    T5 = Label(root, textvariable=t5, bg="#243447", fg='#ffffff')
    T6 = Label(root, textvariable=t6, bg="#243447", fg='#ffffff')
    R1=Button(root, text="Done", bg="#243447", fg='#ffffff', command=get_boxes_and_destroy)

    t1.set('Compliance Standards:')
    T1.place(x=25, y=15)
    C1 = Checkbutton(root, text = "CWE", variable = v1, background="#243447",fg='#ffffff', selectcolor='#000000')
    C2 = Checkbutton(root, text = "CAPEC", variable = v2, background="#243447",fg='#ffffff', selectcolor='#000000')
    C1.place(x=25, y=40)
    C2.place(x=105, y=40)

    t2.set('Security Requirements:')
    T2.place(x=25, y=75)
    t3.set('Confidentiality')
    T3.place(x=25, y=100)
    data=("Low", "Medium", "High")
    global cb1
    cb1=Combobox(root, values=data)
    cb1.place(x=25, y=125)

    t4.set('Integrity')
    T4.place(x=25, y=150)
    data=("Low", "Medium", "High")
    global cb2
    cb2=Combobox(root, values=data)
    cb2.place(x=25, y=175)

    t5.set('Availability')
    T5.place(x=25, y=200)
    data=("Low", "Medium", "High")
    global cb3
    cb3=Combobox(root, values=data)
    cb3.place(x=25, y=225)

    t6.set('Target Distribution')
    T6.place(x=200, y=200)
    data=("None","Low", "Medium", "High")
    global cb4
    cb4=Combobox(root, values=data)
    cb4.place(x=200, y=225)

    R1.place(x=150,y=260)

    root.title('Model Metadata')
    root.geometry("400x300+10+10")
    root.mainloop()
    save_to_xml()


if __name__ == '__main__':
    main()