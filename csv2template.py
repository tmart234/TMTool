""" this script will elements.csv and threats.csv files and convert
 back to a .tb7 file work in progress """

import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog
import shutil
import os
import collections

script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

tm7_path = filedialog.askopenfilename(parent=root, filetypes=[("template tb7 file", "*.tb7")])
template_path = filedialog.askopenfilename(parent=root, filetypes=[("template csv file", "template.csv")])

# copy and rename file extension for tm7 file
folder_path = os.path.join(script_path, "temp_template.xml")
shutil.copy(tm7_path, folder_path)
# parse xml
root = ET.parse(folder_path).getroot()

# TODO: refactor duplicate code!
# deletes temp xml file
def cleanUp(_folder_path):
    if os.path.exists(_folder_path):
        os.remove(_folder_path)
        return
    else:
        print("The temp file does not exist")

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

# take a threat category GUID and look it up in the category dict
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

cats = find_cats()
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
    # get threat categories of threats we are using in the .tb7 file
    # these categories can not contain 0 threats
    for subelem in types.findall('Category'):
        category = subelem.text
        category = cat2str(category, cats)
        # get guid list
        categories.append(category)
#print(categories)

# get threat categories of all the threats we have in csv file
csv_categories = []
with open(template_path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # skip empty rows
        if row[0] == '':
            break
        elif row[0] == 'Threats' or row[0] == 'Category':
            # start at line +2 to get first threat
            line_count += 1
            continue
        elif line_count >= 2:
            csv_categories.append(row[0])
            line_count += 1
            continue
        else:
            break

    # remove duplicates
    csv_categories = list(set(csv_categories))
    categories = list(set(categories))
    # compare both lists
    compare = (set(csv_categories) - set(categories))
    if not compare:
        print('Same categories')
    else:    
        for _string in csv_categories:
            if _string not in categories:
                print('New category found: ' + _string)

# delete temp .xml file created
cleanUp(folder_path)
