## this script will pull all threats and threat categories
## (STRIDE + custom) from a MS TMT template files (.tb7)
## and it will also pull all template's generic + standard elements
## after, it creates 2 CSV files for each

import xml.etree.ElementTree as ET
import csv

root = ET.parse("temp1.xml").getroot()

# pull all Categories from XML
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
#    print(cats)
    return cats

# take the ID and look it up in the category dict
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key

# gets elements (stencils, flows boundarys)
class Elements():
    def __init__(self, root, writer, ele_type):
	    for types in root.iter('ElementType'):
	    	for subelem in types.findall('Name'):
    			self.ele_name = subelem.text
    		for subelem in types.findall('ID'):
    			self.ele_id = subelem.text
    		for subelem in types.findall('Description'):
    			self.ele_desc = subelem.text
    		for subelem in types.findall('ParentElement'):
    			self.ele_parent = subelem.text
    			# WRITE EACH ROW ITERATIVELY
    		writer.writerow([self.ele_name,self.ele_id,self.ele_desc,self.ele_parent,ele_type])




 
cats = find_cats()

with open('threats.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    # write headders in csv file
    writer.writerow(['Category','Short Title','Description'])


    for types in root.iter('ThreatType'):
        # skip row if is a 'root' category
        for subelem in types.findall('Id'):
            _id = subelem.text
        if subelem.text == 'SU':
            continue
        elif subelem.text == 'TU':
            continue
        elif subelem.text == 'RU':
            continue
        elif subelem.text == 'IU':
            continue
        elif subelem.text == 'DU':
            continue
        elif subelem.text == 'EU':
            continue

        # get elements
        for subelem in types.findall('Category'):
            cat = subelem.text
            cat = cat2str(cat, cats)
        for subelem in types.findall('ShortTitle'):
            title = subelem.text
        for subelem in types.findall('Description'):
            desc = subelem.text

        # WRITE EACH ROW ITERATIVELY 
        writer.writerow([cat,title,desc])

with open('elements.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    # write headders in csv file
    writer.writerow(['Name', 'ID', 'Description', 'Parent', 'Element Type'])

    # generic elements
    for gen in root.findall('GenericElements'):
        Elements(root, writer, "Generic")

    # standard elements
    for stan in root.findall('StandardElements'):
        Elements(root, writer, "Standard")
