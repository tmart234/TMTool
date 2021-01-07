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


 
cats = find_cats()

with open('test1.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    # write headders in csv file
    writer.writerow(['Category','Short Title','Description'])


    for types in root.iter('ThreatType'):
        # skip row it is a 'root' category
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
