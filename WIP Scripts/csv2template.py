""" 
This script will take a .tb7 file and template.csv file
It will compare threat categories, individual threats, and threat GUIDs in order
If, there are more or less categories/threats present in template.csv,
that difference will be added or subtracted to the xml and saved as a new .tb7 file
 
work in progress!!!
"""

import csv
import os
import shutil
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import filedialog
import uuid

script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

tm7_path = filedialog.askopenfilename(parent=root, filetypes=[("template tb7 file", "*.tb7")])
csv_path = filedialog.askopenfilename(parent=root, filetypes=[("template csv file", "template.csv")])

# parse xml
tree = ET.parse(tm7_path)
root = tree.getroot()

# take a threat category GUID and look it up in the category dict
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

# TODO: refactor duplicate code!
# deletes temp xml file
def cleanUp(_folder_path):
    if os.path.exists(_folder_path):
        os.remove(_folder_path)
        return
    else:
        print("The temp file does not exist")

# search csv for headder, get colmn values in a list
def get_column(reader, hddr ):
    col1 = []
    col2 = []
    found = False
    for row in reader:
        if row[0] == hddr:
            found = True
            continue
        elif row[0] == '':
            break
        elif found is True:
            col1.append(row[0])
            col2.append(row[1])
            continue
        else:
            break
    return col1, col2

# search csv for headder, get all row values in a list (lists of lists)
def get_rows(_reader, hddr, col_num):
    found = False
    _row = []
    _rows = []
    for row in _reader:
        if row[0] == hddr:
            found = True
            continue
        elif row[0] == '':
            break
        elif found is True:
            # get up to col_num columns
            for i in range(col_num):
                _row.append(row[i])
            _rows.append(row)
            continue
        else:
            break
    return _rows
 

# pull all available threat Categories and their GUIDs from the XML
# some may be empty (contains 0 threats)
def find_cats():
    cats= dict()
    cat_ID=''
    cat_name=''
    for cat in root.iter('ThreatCategory'):
        for subelem in cat.findall('Name'):
            cat_name = subelem.text
        for subelem in cat.findall('Id'):
            cat_ID = subelem.text
        cats[cat_name]=cat_ID
    return cats

# get threats from .tb7 file as dict
def find_threats(root):
    threats = dict()
    title = ''
    _id = ''
    desc = ''
    category = ''
    for threat in root.iter('ThreatType'):
        for subelem in threat.findall('ShortTitle'):
            # remove curley braces for csv output
            title = subelem.text.translate({ord('{'):None, ord('}'):None})
        for subelem in threat.findall('Id'):
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
        for subelem in threat.findall('Description'):
            desc = subelem.text.translate({ord('{'):None, ord('}'):None})
        for subelem in threat.findall('Category'):
            category = cat2str(subelem.text, find_cats())
        threats[_id]=[title,desc,category]
    return threats

# find if an item occures in list
def compare_list(item, _list):
    for _str in _list:
        if item == _str:
            return True
    return False

# add cat to xml file
def add_cat(cat, cats_dict=None):
    new_cat = ET.Element("ThreatCategory")
    name = ET.SubElement(new_cat, 'Name')
    # set category name
    name.text = str(cat)
    
    id_ele = ET.SubElement(new_cat, 'Id')
    if cats_dict is None:
        # generate GUID for category
        id_ele.text = str(uuid.uuid4())
    else:
        # set ID
        id_ele.text = str(cats_dict.get(cat)) 

    ET.SubElement(new_cat, 'ShortDescription')
    ET.SubElement(new_cat, 'LongDescription')
    # insert new element
    root[4].insert(0, new_cat)
    print('added category: ' + cat)

def add_threat():
    return

def add_element():
    return

def delete_cat(cat):
    for item in root[4].iter():
        for subelem in item.findall('Name'):
            if subelem.text == cat:
                root[4].remove(item)
                print('removed category: ' + cat)
    return

def delete_threat(threat):
    return

def delete_element(element):
    return

def compare(surplus, deficit, _type, _list, csv_dict):
    if surplus:
        # add extra to xml file
        print('Adding all '+ _type +' found: ' + str(*surplus))
        for x in surplus:
            if x not in _list:
                if _type == 'categories':
                    add_cat(x, csv_dict)
                elif _type == 'threats':
                    add_threat(x, csv_dict)
                elif _type == 'threats':
                    add_element(x, csv_dict)
                else:
                    print('bad type. Chose type from categories, threats, or stencils')
            else:
                print('error adding. Chekck lists')
                print(*_list)
    if deficit:
        for x in deficit:
        # remove missing from xml file
            print('Removing all '+ _type+' found: ' + str(*deficit))
            if x in _list:
                if _type == 'categories':
                    delete_cat(x)
                elif _type == 'threats':
                    delete_threat(x)
                elif _type == 'threats':
                    delete_element(x, csv_dict)
                else:
                    print('bad type. Chose type from categories, threats, or stencils')
            else:
                print('error removing. Chekck lists')
                print(*_list)

# get csv threat categories & id as dict
def find_csv_cats(_reader):
    keys,values = get_column(_reader, 'Threat Categories')
    cats = dict(zip(keys,values))
    return cats
    
# get csv threats as dict
def find_csv_threats(_reader):
    threat_list = get_rows(_reader, 'Threat Title', 6)
    threats = dict()
    key = ''
    value = []
    for threat in threat_list:
        # guid as key
        key = threat[2]
        # everything else as values
        value = [threat[0], threat[1], threat[3]]
        threats.update({key:value})
    return threats


categories = list(find_cats().keys())

with open(csv_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    csv_cats = find_csv_cats(csv_reader)
    csv_categories = list(csv_cats.keys())
    # compare both category lists
    print('comparing categories...' )
    surplus = list(sorted(set(csv_categories) - set(categories)))
    deficit = list(sorted(set(categories) - set(csv_categories)))
    print(categories)
    if not surplus and not deficit:
        print('Same categories')
    else:
        # modify xml file
        compare(surplus, deficit, 'categories', categories, csv_cats)

    threat_ids = list(find_threats().keys())
    csv_threats = find_csv_threats(csv_reader)
    csv_threat_ids = list(csv_cats.keys())
    print('comparing threats...' )
    surplus = list(sorted(set(csv_threat_ids) - set(threat_ids)))
    deficit = list(sorted(set(threat_ids) - set(csv_threat_ids)))
    print(csv_threats)
    if not surplus and not deficit:
        print('Same threats')
    else:
        # modify xml file
        compare(surplus, deficit, 'threats', threat_ids, csv_threats)

    # TODO: compare individual threats by "short title", add/sub to xml
    # TODO: compare guids, always choose template.csv's guid for any non matching guids

# TODO: remove and replace with function that copies to new .tb7 file
tree.write(tm7_path)
