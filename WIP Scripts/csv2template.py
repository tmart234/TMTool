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
from tkinter.constants import LAST
import uuid

script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

tm7_path = filedialog.askopenfilename(parent=root, filetypes=[("template tb7 file", "*.tb7")])
csv_path = filedialog.askopenfilename(parent=root, filetypes=[("template csv file", "template.csv")])

# copy and rename file extension for tm7 file
folder_path = os.path.join(script_path, "temp_template.xml")
shutil.copy(tm7_path, folder_path)
# parse xml
tree = ET.parse(folder_path)
root = tree.getroot()

# TODO: refactor duplicate code!
# deletes temp xml file
def cleanUp(_folder_path):
    if os.path.exists(_folder_path):
        os.remove(_folder_path)
        return
    else:
        print("The temp file does not exist")

# search csv for headder, get colmn values in a list
def get_column(reader, hddr, col):
    csv_column = []
    found = False
    for row in reader:
        if row[col] == hddr:
            found = True
            continue
        elif found is True:
            csv_column.append(row[col])
            continue
        else:
            break
    return csv_column
 

# pull all available threat Categories and their GUIDs from the XML
# some may be empty (contains 0 threats)
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

# find if an item occures in list
def compare_list(item, _list):
    for _str in _list:
        if item == _str:
            return True
    return False

# add cat to xml file
def add_cat(cat, cats):
    new_cat = ET.Element("ThreatCategory")
    name = ET.SubElement(new_cat, 'Name')
    # set category name
    name.text = str(cat)
    id = ET.SubElement(new_cat, 'Id')
    # generate GUID for category
    id.text = str(uuid.uuid4())

    ET.SubElement(new_cat, 'ShortDescription')
    ET.SubElement(new_cat, 'LongDescription')
    # insert new element
    root[4].insert(0, new_cat)
    print('added category: ' + cat)


# loop each list, compare, and add if not found
def compare_cats(_surplus, _cats):
    for item in _surplus:
    # compare each category in surplus list
        result = compare_list(item, _cats)
        # dont compare category GUIDs
        if result == True:
            continue
    # add surplus category
        else:
            print('Threat category not found: ' + item)
            add_cat(item, _cats)
    return

# take a threat category GUID and look it up in the category dict
def guid2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

# # take a threat category and look up it's GUID in the dict
def str2guid(cat, cats):
    for key, value in cats.items():
        if cat == key:
            return value

cats = find_cats()
# print(cats)
categories = []
# enumerate temp_xml threats categories
for types in root.iter('ThreatType'):
        # get ID and skip row if ID is a 'root' category
    _id = ''
    category = ''
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
    # TODO: redo this
    # get threat categories of threats we are using in the .tb7 file
    # these categories can not contain 0 threats
    for subelem in types.findall('Category'):
        category = subelem.text
        category = guid2str(category, cats)
        # get guid list
        categories.append(category)
#print(categories)

with open(csv_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    # get threat category names of all the threats we have in csv file
    csv_categories = get_column(csv_reader, 'Threat Categories', 1)

    # compare both category lists
    print('comparing categories...' )
    surplus = list(set(set(csv_categories) - set(categories)))
    deficit = list(set(set(categories) - set(csv_categories)))
    if not surplus and not deficit:
        print('Same categories')
    # modify xml file here
    else:
        # add extra csv categories
        if surplus and surplus not in categories:
            print('Adding all threats from categories found: ' + str(surplus))
            key_cats = []
            for keys,value in cats.items():
                key_cats.append(keys)
            if key_cats and surplus:
                # loop each list, compare, and add if not found
                compare_cats(surplus, cats)
            else:
                print('empty lists')
                print(key_cats)

        # TODO: make work with deficit
        # remove missing csv category threats
        if deficit and deficit not in csv_categories:
            print('Removing all threats from category not found: ' + str(deficit))
            # delete each threat in deficit's category list
            # remove category entirely if not STRIDE

    # TODO: compare individual threats by "short title", add/sub to xml
    # TODO: compare guids, always choose template.csv's guid for any non matching guids

# TODO: remove and replace with function that copies to new .tb7 file
tree.write(folder_path)
#cleanUp(folder_path)
