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
folder_path = str(os.path.join(script_path, "temp_template.xml"))
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
    column1 = []
    column2 = []
    found = False
    for row in reader:
        if row[col] == hddr:
            found = True
            continue
        elif row[col] == '':
            break
        elif found is True:
            column1.append(row[col])
            column2.append(row[(col+1)])
            continue
        else:
            break
    return column1, column2
 

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

def delete_cat(cat):
    for item in root[4].iter():
        for subelem in item.findall('Name'):
            if subelem.text == cat:
                root[4].remove(item)
                print('removed category: ' + cat)
    return

def compare_cats(surplus, deficit, csv_cats):
    if surplus:
        # add extra csv categories
        print('Adding all threats from categories found: ' + str(*surplus))
        for x in surplus:
            if x not in categories:
                add_cat(x, csv_cats)
            else:
                print('error adding')
    if deficit:
        for x in deficit:
        # remove missing csv categories from template file
            print('Removing all threats from category not found: ' + str(*deficit))
            if x in categories:
                # loop each list, compare, and add if not found
                delete_cat(x)
            else:
                print('error with deficit lists')
                print(*categories)

# take a threat category GUID and look it up in the category dict
def guid2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

# get csv threat categories & id as dict
def find_csv_cats(_reader):
    keys,values = get_column(_reader, 'Threat Categories', 0)
    cats = dict(zip(keys,values))
    return cats

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
        compare_cats(surplus, deficit, csv_cats)

    # TODO: compare individual threats by "short title", add/sub to xml
    # TODO: compare guids, always choose template.csv's guid for any non matching guids

# TODO: remove and replace with function that copies to new .tb7 file
tree.write(folder_path)
#cleanUp(folder_path)
