## this script will pull all threats and threat categories
## (STRIDE + custom) from a MS TMT template files (.tb7)
## and it will also pull all template's generic + standard elements
## after, it creates a template.csv file

import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog
import shutil
import os

# get script's path
script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS threat template files", "*.tb7")])
# copy and rename file extension
folder_path = os.path.join(script_path, "temp_template.xml")
shutil.copy(file_path, folder_path)

root = ET.parse(folder_path).getroot()

# pull all threat Categories and their GUIDs from the XML
def find_cats():
    cats={}
    cat_ID=''
    cat_name=''
    for cat in root.iter('ThreatCategory'):
        for subelem in cat.findall('Name'):
            cat_name = subelem.text
        for subelem in cat.findall('Id'):
            cat_ID = subelem.text
        cats[cat_name]=cat_ID
    return cats


# take a threat category GUID and look it up in the category dict
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

# deletes temp xml file
def cleanUp(_folder_path):
    if os.path.exists(_folder_path):
        os.remove(_folder_path)
        return
    else:
        print("The temp file does not exist")
        return

# gets elements (stencils, flows boundarys)
class Elements():
    def __init__(self, root, writer, ele_type):
            for _type in root.findall(ele_type):
                for types in _type.iter('ElementType'):
                    for subelem in types.findall('Name'):
                            self.ele_name = subelem.text
                    for subelem in types.findall('ID'):
                            self.ele_id = subelem.text
                    for subelem in types.findall('Description'):
                            self.ele_desc = subelem.text
                    for subelem in types.findall('ParentElement'):
                            self.ele_parent = subelem.text
                    for subelem in types.findall('Hidden'):
                            self.hidden = subelem.text
                    for subelem in types.findall('Representation'):
                            self.rep = subelem.text
                    # will not get <Image>, <StrokeThickness>, <ImageLocation>, or sencil constraints
                            # TODO: get attributes
                    writer.writerow([self.ele_name,self.ele_id,self.ele_desc,self.ele_parent,self.hidden,self.rep])

 
cats = find_cats()

with open('template.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    # write headders in csv file
    writer.writerow(['Threats'])
    writer.writerow(['Category','Short Title','Description', 'Include Logic', 'Exclude Logic'])

    for types in root.iter('ThreatType'):
        # get ID and skip row if ID is a 'root' category
        _id = ''
        for subelem in types.findall('Id'):
            _id = subelem.text
        if _id == 'SU':
            continue
        elif _id == 'TU':
            continue
        elif _id == 'RU':
            continue
        elif _id == 'IU':
            continue
        elif _id == 'DU':
            continue
        elif _id == 'EU':
            continue

        # TODO: replace threat logic GUIDs with names in csv and make a guid lookup function for elements
        # get threat logic
        for gen_filters in types.findall('GenerationFilters'):
            for include_logic in gen_filters.findall('Include'):
                include = include_logic.text
            for exclude_logic in gen_filters.findall('Exclude'):
                exclude = exclude_logic.text
        # get elements
        for subelem in types.findall('Category'):
            category = subelem.text
            category = cat2str(category, cats)
        for subelem in types.findall('ShortTitle'):
            # remove curley braces for csv output
            title = subelem.text.translate({ord('{'):None, ord('}'):None})
        for subelem in types.findall('Description'):
            desc = subelem.text.translate({ord('{'):None, ord('}'):None})

        # WRITE EACH ROW ITERATIVELY 
        writer.writerow([category,title.replace(".Name",""),desc.replace(".Name",""),include,exclude])

    writer.writerow('')
    writer.writerow(['Generic Elements'])
    writer.writerow(['Name', 'ID', 'Description','Parent', 'Hidden_bool', 'Representation'])

    # generic elements
    Elements(root, writer, "GenericElements")

    writer.writerow('')
    writer.writerow(['Standard Elements'])
    writer.writerow(['Name', 'ID', 'Description','Parent', 'Hidden_bool', 'Representation'])

    # standard elements
    Elements(root, writer, "StandardElements")

    # delete temp .xml file created
    cleanUp(folder_path)