""" this script will pull all threats and  generic + standard elements 
from a MS TMT template files (.tb7). after, it creates a sqlite database
 Work in progress!!! """

import xml.etree.ElementTree as ET
import tkinter as tk
from tkinter import filedialog
import shutil
import os
import xmltodict
import json
import sqlite3

namespaces = {
        'http://www.w3.org/2001/XMLSchema-instance': None # skip this namespace
        }

# create 2 tables: threats, and elements
def addTable(dbcur, table):
    if table == 'threats':
        dbcur.execute('''CREATE TABLE IF NOT EXISTS threats
                    (category, title, ID, description, in_logic, ex_logic)''')
    elif table == 'elements':
        dbcur.execute('''CREATE TABLE IF NOT EXISTS elements
                    (name, ID, description, parent, hidden_bool, representation, type)''')
    else:
        print('Error creating tables!')
    return

# take a threat category GUID and look it up in the category dict
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

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

# writes all template threats to database
def write_threats(root, cur):
    cats = find_cats()
    category=threat_id=title=desc=include=exclude=prop_str = str()
    for types in root.iter('ThreatType'):
        # TODO: replace threat logic GUIDs with names in csv and make a guid lookup function for elements
        # get threat logic
        for gen_filters in types.findall('GenerationFilters'):
            for include_logic in gen_filters.findall('Include'):
                include = str(include_logic.text)
                include = include.replace("'", "")
            for exclude_logic in gen_filters.findall('Exclude'):
                exclude = str(exclude_logic.text)
                exclude = exclude.replace("'", "")
        # get elements
        for subelem in types.findall('Category'):
            category = cat2str(subelem.text, cats)
        for subelem in types.findall('Id'):
            threat_id = subelem.text
        for subelem in types.findall('ShortTitle'):
            # remove curley braces for output
            title = subelem.text.translate({ord('{'):None, ord('}'):None})
            title = title.replace(".Name","")
            title = title.replace("'", "")
        for subelem in types.findall('Description'):
            desc = subelem.text.translate({ord('{'):None, ord('}'):None})
            desc = desc.replace(".Name","")
            desc = desc.replace("'", "")
        # get all property data (all child elements)
        # properties = types.find('PropertiesMetaData')
        # prop_str = ET.tostring(properties, encoding='utf8', method='xml')
        # # have to dump as json because we have an ordereddicts within ordereddicts
        # prop_str = str(json.loads(json.dumps(xmltodict.parse(prop_str,process_namespaces=True,namespaces=namespaces))))
        # TODO: get element constraints?
        # build sql string
        search = str("\'" + category +"\',\'"+title+"\',\'"+threat_id+"\',\'"+ desc + "\',\'" +include+ "\',\'" +exclude+ "\'")
        search = str("INSERT INTO threats VALUES (" + search + ")")
        cur.execute(search)

# gets elements (stencils, flows boundarys)
class Elements():
    def __init__(self, root, cur, ele_type):
            for _type in root.findall(ele_type):
                for types in _type.iter('ElementType'):
                    for subelem in types.findall('Name'):
                            self.ele_name = str(subelem.text)
                    for subelem in types.findall('ID'):
                            self.ele_id = str(subelem.text)
                    for subelem in types.findall('Description'):
                            self.ele_desc = str(subelem.text)
                            self.ele_desc = self.ele_desc.replace("'", "")
                    for subelem in types.findall('ParentElement'):
                            self.ele_parent = str(subelem.text)
                    for subelem in types.findall('Hidden'):
                            self.hidden = str(subelem.text)
                    for subelem in types.findall('Representation'):
                            self.rep = str(subelem.text)
                    # will not get <Image>, <StrokeThickness>, <ImageLocation>, or sencil constraints
                            # get all property data (all child elements)
                    elemnent_attribs = types.find('Attributes')
                    self.attribs = ET.tostring(elemnent_attribs, encoding='utf8', method='xml')
                    # have to dump as json because we have an ordereddicts within ordereddicts
                    self.attribs = json.loads(json.dumps(xmltodict.parse(self.attribs,process_namespaces=True,namespaces=namespaces)))
                    search = str("\'" + self.ele_name +"\',\'"+self.ele_id+"\',\'"+self.ele_desc+"\',\'"+ self.ele_parent + "\',\'" +self.hidden+ "\',\'" +self.rep + "\',\'" +  ele_type+ "\'")
                    search = str("INSERT INTO elements VALUES (" + search + ")")
                    cur.execute(search)

# get script's path
script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
# hide root window
root.withdraw()
file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS threat template files", "*.tb7")])
# copy and rename file extension
folder_path = os.path.join(script_path, "temp_template.xml")
shutil.copy(file_path, folder_path)

root = ET.parse(folder_path).getroot()

conn = sqlite3.connect('test.db')
cur = conn.cursor()
tables = ['threats','elements']
for x in tables:
    addTable(cur, x)
# get threats and write to database
write_threats(root, cur)
# get elements and write to database
Elements(root, cur, "GenericElements")
Elements(root, cur, "StandardElements")

# Save the changes
conn.commit()
# close the connection if we are done with it
conn.close()
