""" 
This script will take a .tb7 file and template.xlsx file
It will compare threat categories, individual threats, and threat GUIDs in order
If, there are more or less categories/threats present in template.xlsx,
that difference will be added or subtracted to the xml and saved as a new .tb7 file
"""

import os
import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import filedialog
import uuid
import openpyxl

# take a threat category GUID and look it up in the category dict
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key
    return None

# take a threat category GUID and look it up in the category dict
def cat2guid(cat, cats):
    for key, value in cats.items():
         if cat == key:
             return value
    return None

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
def find_cats(root):
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
    _id = ''
    title = ''
    desc = ''
    category = ''
    for threat in root.iter('ThreatType'):
        for subelem in threat.findall('ShortTitle'):
            # remove curley braces for xlsx output
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
            category = cat2str(subelem.text, find_cats(root))
        threats[_id]=[title,desc,category]
    return threats

# get all elements from .tb7 file as dict
def find_elements(root):
    name = ''
    _id = ''
    desc = ''
    parent = ''
    hidden = ''
    rep = ''
    elements = dict()
    #element = dict().fromkeys({'Stencil Name', 'Type', 'ID', 'Description','Parent', 'Hidden_bool', 'Representation', 'Attributes'})
    _type = 'GenericElements'
    for ele in root.findall(_type):
        for subelem in ele.findall('ElementType'):
            for subelem2 in subelem.findall('ID'):
                _id = str(subelem2.text)
            for subelem2 in subelem.findall('Name'):
                name = str(subelem2.text)
            for subelem2 in subelem.findall('Description'):
                desc = str(subelem2.text)
            for subelem2 in subelem.findall('ParentElement'):
                parent = str(subelem2.text)    
            for subelem2 in subelem.findall('Hidden'):
                hidden = str(subelem2.text)    
            for subelem2 in subelem.findall('Representation'):
                rep = str(subelem2.text)   
            elements[_id]=[name,_type,_id, desc, parent, hidden, rep]
    _type = 'StandardElements'
    for ele in root.findall(_type):
        for subelem in ele.findall('ElementType'):
            for subelem2 in subelem.findall('ID'):
                _id = str(subelem2.text)
            for subelem2 in subelem.findall('Name'):
                name = str(subelem2.text)
            for subelem2 in subelem.findall('Description'):
                desc = str(subelem2.text)
            for subelem2 in subelem.findall('ParentElement'):
                parent = str(subelem2.text)    
            for subelem2 in subelem.findall('Hidden'):
                hidden = str(subelem2.text)    
            for subelem2 in subelem.findall('Representation'):
                rep = str(subelem2.text)   
            elements[_id]=[name,_type,_id, desc, parent, hidden, rep]
    return elements

# add cat to xml file
def add_cat(root, cat, cats_dict=None):
    _uuid = ''
    new_cat = ET.Element("ThreatCategory")
    name = ET.SubElement(new_cat, 'Name')
    # set category name
    name.text = str(cat)
    
    id_ele = ET.SubElement(new_cat, 'Id')
    if cats_dict.get(cat) is None:
        # generate GUID for category
        _uuid = str(uuid.uuid4())
        id_ele.text = _uuid
    else:
        # set ID
        id_ele.text = str(cats_dict.get(cat))
        _uuid = str(id_ele.text)

    ET.SubElement(new_cat, 'ShortDescription')
    ET.SubElement(new_cat, 'LongDescription')
    # insert new element
    root[4].insert(0, new_cat)
    print('added category: ' + cat)
    return _uuid

# find threat from id in xlsx_threat_dict and add to .tb7
def add_threat(root, threat_id, threats):
    threat = threats.get(threat_id)
    new_threat = ET.Element("ThreatType")

    _uuid = ''
    filter = ET.SubElement(new_threat, 'GenerationFilters')
    include_ele = ET.SubElement(filter, 'Include')
    include_ele.text = threat.get('Include Logic')
    exclude_ele = ET.SubElement(filter, 'Exclude')
    exclude_ele.text = threat.get('Exclude Logic')
    # check id
    id_ele = ET.SubElement(new_threat, 'Id')
    if threat.get('Id') is None:
        # generate GUID if not present
        _uuid = str(uuid.uuid4())
        id_ele.text = _uuid
    else:
        # sets to ID if present
        id_ele.text = threat_id

    name = ET.SubElement(new_threat, 'ShortTitle')
    # set threat name
    name.text = threat.get('Threat Title')

    cat = ET.SubElement(new_threat, 'Category')
    # set as cat guid
    _cat = cat2guid(threat.get('Category'),find_cats(root))
    if not _cat:
        # add if it does not exist
        print('warning no category found: '+ threat.get('Category'))
        # 
        _cat = add_cat(root, threat.get('Category'),find_cats(root))
    cat.text = _cat
    ET.SubElement(new_threat, 'RelatedCategory')  

    desc = ET.SubElement(new_threat, 'Description')
    desc.text = threat.get('Description')
    ET.SubElement(new_threat, 'PropertiesMetaData')
    # insert new threat
    root[5].insert(0, new_threat)
    print('added threat: ' + str(name.text) + ' ' + str(id_ele.text))
    return _uuid

# find threat from id in xlsx_threat_dict and add to .tb7
def add_element(root, ele_id, elements, _type):
    element = elements.get(ele_id)
    new_ele = ET.Element("ElementType")
    _uuid = ''
    name = ET.SubElement(new_ele, 'Name')
    name.text = element.get('Stencil Name')
    # check id
    id_ele = ET.SubElement(new_ele, 'Id')
    if element.get('ID') is None:
        # generate GUID if not present
        _uuid = str(uuid.uuid4())
        id_ele.text = _uuid
    else:
        # sets to ID if present
        id_ele.text = ele_id

    desc = ET.SubElement(new_ele, 'Description')
    desc.text = element.get('Description')

    parent = ET.SubElement(new_ele, 'ParentElement')
    parent.text = element.get('Parent')
    
    ET.SubElement(new_ele, 'Image')  
    desc = ET.SubElement(new_ele, 'Hidden')
    desc.text = element.get('Hidden_bool')
    ET.SubElement(new_ele, 'Representation')
    desc.text = element.get('Representation')

    ticc = ET.SubElement(new_ele, 'StrokeThickness')
    ticc.text = '0'
    loc = ET.SubElement(new_ele, 'ImageLocation')
    # default values
    loc.text = 'Centered on stencil'
    ET.SubElement(new_ele, 'Attributes')
    ET.SubElement(new_ele, 'StencilConstraint')
    # insert new threat
    if str(element.get('Type')) == 'GenericElements':
        root[2].insert(0, new_ele)
    elif str(element.get('Type')) == 'StandardElements':
        root[3].insert(0, new_ele)
    else:
        print('bad element type. Chose GenericElements or StandardElements')
    print('added element: ' + str(name.text) + ' ' + str(id_ele.text))
    return _uuid

def delete_cat(root, cat):
    for item in root[4].iter():
        for subelem in item.findall('Name'):
            if subelem.text == cat:
                root[4].remove(item)
                print('removed category: ' + cat)
    return

# deletes threat based on threat_id
def delete_threat(root, threat_id):
    for item in root[5].iter():
        for subelem in item.findall('Id'):
            if subelem.text == threat_id:
                root[5].remove(item)
                print('removed threat: ' + threat_id)
    return

# deletes element/stencil based on ele_id
def delete_element(root, ele_id):
    for item in root[3].iter():
        for subelem in item.findall('Id'):
            if subelem.text == ele_id:
                root[3].remove(item)
                print('removed element: ' + ele_id)
    for item in root[4].iter():
        for subelem in item.findall('Id'):
            if subelem.text == ele_id:
                root[4].remove(item)
                print('removed element: ' + ele_id)
    return

def compare(root, surplus, deficit, _type, _list, xlsx_dict):
    if surplus:
        # add extra to xml file
        print('Adding all '+ _type +' found: ' + str(surplus))
        for x in surplus:
            if x not in _list:
                if str(_type) == 'categories':
                    add_cat(root, x, xlsx_dict)
                elif str(_type) == 'threats':
                    add_threat(root, x, xlsx_dict)
                elif str(_type) == 'stencils':
                    add_element(root, x, xlsx_dict, _type)
                else:
                    print('bad type. Chose type from categories, threats, or stencils')
            else:
                print('error adding. Chekck lists')
                print(*_list)
    if deficit:
        print('Removing all '+ _type+' found: ' + str(deficit))
        for x in deficit:
        # remove missing from xml file
            if x in _list:
                if _type == 'categories':
                    delete_cat(root, x)
                elif _type == 'threats':
                    delete_threat(root, x)
                elif _type == 'threats':
                    delete_element(root, x, xlsx_dict)
                else:
                    print('bad type. Chose type from categories, threats, or stencils')
            else:
                print('error removing. Chekck lists')
                print(*_list)
    
# returns xlsx threats as dict of threats (dict of dicts)
def find_xlsx_threats(wb):
    sheet = wb['Threats']
    threats = dict()
    threat = dict().fromkeys({'Threat Title','Category','ID','Description', 'Include Logic', 'Exclude Logic','Properties'})
    _id = ''
    for _row in range(2,(int(sheet.max_row)+1)):
        for _col in range(1,int(sheet.max_column)):
            cell = sheet.cell(row=_row, column=_col).value
            if _col == 1:
                threat['Threat Title'] = cell
            elif _col == 2:
                threat['Category'] = cell
            elif _col == 0:
                _id = cell
                threat['ID'] = _id
            elif _col == 4:
                threat['Description'] = cell
            elif _col == 5:
                threat['Include Logic'] = cell
            elif _col == 6:
                threat['Exclude Logic'] = cell
            else:
                print("error reading xlsx!")
        # add to dict with guid as key
        threats[_id] = threat
    return threats

# returns xlsx elements as dict of elements (dict of dicts)
def find_xlsx_elements(wb):
    sheet = wb['Stencils']
    _id = ''
    elements = dict()
    element = dict().fromkeys({'Stencil Name', 'Type', 'ID', 'Description','Parent', 'Hidden_bool', 'Representation', 'Attributes'})
    for _row in range(2,(int(sheet.max_row)+1)):
            for _col in range(1,int(sheet.max_column)):
                cell = sheet.cell(row=_row, column=_col).value
                if _col == 0:
                    element['Stencil Name'] = cell
                elif _col == 1:
                    element['Type'] = cell
                elif _col == 2:
                    _id = cell
                    element['ID'] = _id
                elif _col == 3:
                    element['Description'] = cell
                elif _col == 4:
                    element['Prent'] = cell
                elif _col == 5:
                    element['Hidden_bool'] = cell
                elif _col == 6:
                    element['Representation'] = cell
                elif _col == 7:
                    element['Attributes'] = cell
                else:
                    print("error reading xlsx! 2")
            elements[_id] = element
    return elements
    
def main():
    root = tk.Tk()
    root.withdraw()

    xlsx_path = None
    tm7_path = None
    try:
        xlsx_path = filedialog.askopenfilename(parent=root, filetypes=[("template xlsx file", "template.xlsx")])
        tm7_path = filedialog.askopenfilename(parent=root, filetypes=[("template tb7 file", "*.tb7")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    root.destroy()
    # create 2nd file till script is g2g
    if not xlsx_path and tm7_path:
        print('Must choose file path, quitting... ')
        quit()
    # Open Workbook
    wb = openpyxl.load_workbook(filename=xlsx_path, data_only=True)

    # parse xml
    tree = ET.parse(tm7_path)
    root = tree.getroot()

    # Get All Sheets
    a_sheet_names = wb.sheetnames
    # check for sheets
    if ('Metadata' and 'Threats' and 'Stencils') in a_sheet_names:
        print("All Sheets found!")
    else:
        print("Error! xlxs worksheets missing")
        quit()

    #xlsx_cats = find_xlsx_cats(wb)
    #xlsx_categories = list(xlsx_cats.keys())

    threat_ids = list(find_threats(root).keys())
    xlsx_threats = find_xlsx_threats(wb)
    xlsx_threat_ids = list(xlsx_threats.keys())
    print('comparing threats...' )
    surplus = list(sorted(set(xlsx_threat_ids) - set(threat_ids)))
    deficit = list(sorted(set(threat_ids) - set(xlsx_threat_ids)))
    if not surplus and not deficit:
        print('Same threats')
    else:
        # modify xml file
        compare(root, surplus, deficit, 'threats', threat_ids, xlsx_threats)

    element_ids = list(find_elements(root).keys())
    xlsx_elements = find_xlsx_elements(wb)
    xlsx_element_ids = list(xlsx_elements.keys())
    print('comparing elements...')
    surplus = list(sorted(set(xlsx_element_ids) - set(element_ids)))
    deficit = list(sorted(set(element_ids) - set(xlsx_element_ids)))
    if not surplus and not deficit:
        print('Same elements')
    else:
        # modify xml file
        compare(root, surplus, deficit, 'stencils', element_ids, xlsx_elements)

    print('Finished!')
    #TODO: remove
    tm7_path = tm7_path.replace('.tb7','2.tb7')
    tree.write(tm7_path)

if __name__ == '__main__':
    main()
