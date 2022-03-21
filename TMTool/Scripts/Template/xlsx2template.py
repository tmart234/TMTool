""" 
This script will attempt to convert all information from a 
TMTool template.xlsx file into a MS TMT template file (.tb7)
"""

import os
import tkinter as tk
from lxml.etree import Element, SubElement, ElementTree
from tkinter import filedialog
import uuid
import openpyxl

# take a threat category GUID and look it up in the category dict
#TODO: delete
def cat2str(cat, cats):
    for key, value in cats.items():
         if cat == value:
             return key
    return None

# take a threat category GUID and look it up in the category dict
#TODO: delete
def cat2guid(cat, cats):
    for key, value in cats.items():
         if cat == key:
             return value
    return None

# deletes temp xml file
#TODO: delete
def cleanUp(_folder_path):
    if os.path.exists(_folder_path):
        os.remove(_folder_path)
        return
    else:
        print("The temp file does not exist")

# pull all available threat Categories and their GUIDs from the XML
# some may be empty (contains 0 threats)
#TODO: delete
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
    new_cat = Element("ThreatCategory")
    name = SubElement(new_cat, 'Name')
    # set category name
    name.text = str(cat)
    
    id_ele = SubElement(new_cat, 'Id')
    if cats_dict.get(cat) is None:
        # generate GUID for category
        _uuid = str(uuid.uuid4())
        id_ele.text = _uuid
    else:
        # set ID
        id_ele.text = str(cats_dict.get(cat))
        _uuid = str(id_ele.text)

    SubElement(new_cat, 'ShortDescription')
    SubElement(new_cat, 'LongDescription')
    # insert new element
    root[4].insert(0, new_cat)
    print('added category: ' + cat)
    return _uuid

# find threat from id in xlsx_threat_dict and add to .tb7
def add_threat(root, threat_id, threats):
    threat = threats.get(threat_id)
    new_threat = Element("ThreatType")

    _uuid = ''
    filter = SubElement(new_threat, 'GenerationFilters')
    include_ele = SubElement(filter, 'Include')
    include_ele.text = threat.get('Include Logic')
    exclude_ele = SubElement(filter, 'Exclude')
    exclude_ele.text = threat.get('Exclude Logic')
    # check id
    id_ele = SubElement(new_threat, 'Id')
    if threat.get('Id') is None:
        # generate GUID if not present
        _uuid = str(uuid.uuid4())
        id_ele.text = _uuid
    else:
        # sets to ID if present
        id_ele.text = threat_id

    name = SubElement(new_threat, 'ShortTitle')
    # set threat name
    name.text = threat.get('Threat Title')

    cat = SubElement(new_threat, 'Category')
    # set as cat guid
    _cat = cat2guid(threat.get('Category'),find_cats(root))
    if not _cat:
        # add if it does not exist
        print('warning no category found: '+ threat.get('Category'))
        # 
        _cat = add_cat(root, threat.get('Category'),find_cats(root))
    cat.text = _cat
    SubElement(new_threat, 'RelatedCategory')  

    desc = SubElement(new_threat, 'Description')
    desc.text = threat.get('Description')
    SubElement(new_threat, 'PropertiesMetaData')
    # insert new threat
    root[5].insert(0, new_threat)
    print('added threat: ' + str(name.text) + ' ' + str(id_ele.text))
    return _uuid

# find threat from id in xlsx_threat_dict and add to .tb7
def add_element(root, ele_id, elements, _type):
    element = elements.get(ele_id)
    new_ele = Element("ElementType")
    _uuid = ''
    name = SubElement(new_ele, 'Name')
    name.text = element.get('Stencil Name')
    # check id
    id_ele = SubElement(new_ele, 'Id')
    if element.get('ID') is None:
        # generate GUID if not present
        _uuid = str(uuid.uuid4())
        id_ele.text = _uuid
    else:
        # sets to ID if present
        id_ele.text = ele_id

    desc = SubElement(new_ele, 'Description')
    desc.text = element.get('Description')

    parent = SubElement(new_ele, 'ParentElement')
    parent.text = element.get('Parent')
    
    SubElement(new_ele, 'Image')  
    desc = SubElement(new_ele, 'Hidden')
    desc.text = element.get('Hidden_bool')
    SubElement(new_ele, 'Representation')
    desc.text = element.get('Representation')

    ticc = SubElement(new_ele, 'StrokeThickness')
    ticc.text = '0'
    loc = SubElement(new_ele, 'ImageLocation')
    # default values
    loc.text = 'Centered on stencil'
    SubElement(new_ele, 'Attributes')
    SubElement(new_ele, 'StencilConstraint')
    # insert new threat
    if str(element.get('Type')) == 'GenericElements':
        root[2].insert(0, new_ele)
    elif str(element.get('Type')) == 'StandardElements':
        root[3].insert(0, new_ele)
    else:
        print('bad element type. Chose GenericElements or StandardElements')
    print('added element: ' + str(name.text) + ' ' + str(id_ele.text))
    return _uuid

#TODO: refactor
def delete_cat(root, cat):
    for item in root[4].iter():
        for subelem in item.findall('Name'):
            if subelem.text == cat:
                root[4].remove(item)
                print('removed category: ' + cat)
    return

# deletes threat based on threat_id
#TODO: refactor
def delete_threat(root, threat_id):
    for item in root[5].iter():
        for subelem in item.findall('Id'):
            if subelem.text == threat_id:
                root[5].remove(item)
                print('removed threat: ' + threat_id)
    return

# deletes element/stencil based on ele_id
#TODO: refactor
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

#TODO: delete
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

def get_manifest(root, ws):
    _name = ''
    _id = ''
    _ver = ''
    _author = ''
    for row in ws.iter_rows():
        for cell in row:
            if cell.value == "Template name:":
                # find Tag cell, then get the cell value that's next to the current cell
                _name = ws.cell(row=cell.row,column=(cell.column + 1)).value
            elif cell.value == "Template id:":
                _id = ws.cell(row=cell.row,column=(cell.column + 1)).value
            elif cell.value == "Template version:":
                _ver = ws.cell(row=cell.row,column=(cell.column + 1)).value
            elif cell.value == "Template author:":
                _author = ws.cell(row=cell.row,column=(cell.column + 1)).value
    SubElement(root, 'Manifest', name=_name, id=_id, version=_ver, author=_author)
    return root

# gets threat categories from the metadata worksheet
# TODO: rather with static columns; a better approach would be to find which column "Threat Categories" is in
# then search in with iter_rows(min_col= found_col, max_col=found_col). Could help avoid breaking template changes
def get_threat_categories(xml, ws):
    found = False
    root_category = SubElement(xml, 'ThreatCategories')
    for row in ws.iter_rows(max_col=1):
        for cell in row:
            if found == True:
                if cell.value is not None:
                    category = SubElement(root_category, 'ThreatCategory')
                    SubElement(category, 'Name').text = cell.value
                    # get cell next to current cell
                    SubElement(category, 'Id').text = ws.cell(row=cell.row,column=(cell.column + 1)).value
                    SubElement(category, 'ShortDescription')
                    SubElement(category, 'LongDescription')
                else:
                    return xml
            elif cell.value == "Threat Categories":
                found = True
                continue
    print("Getting threat categories failed")
    return None
 
def get_Threat_Meta(xml, ws):
    found = False
    find_list = ["Is Priority Used", "Is Status Used", "Threat Properties MetaData"]
    root_category = SubElement(xml, 'ThreatMetaData')
    props = SubElement(root_category, 'PropertiesMetaData')
    for row in ws.iter_rows(max_col=1):
        for cell in row:
            if str(cell.value) in find_list:
                if cell.value == "Is Priority Used":
                    SubElement(root_category, 'IsPriorityUsed').text = ws.cell(row=cell.row,column=(cell.column + 1)).value
                elif cell.value == "Is Status Used":
                    SubElement(root_category, 'IsStatusUsed').text = ws.cell(row=cell.row,column=(cell.column + 1)).value
                else:
                    found = True
                    continue
            elif found:
                datum = SubElement(props, 'ThreatMetaDatum')
                SubElement(datum, 'Name').text = cell.value
                SubElement(datum, 'Label').text = ws.cell(row=cell.row,column=(cell.column + 1)).value
                SubElement(datum, 'Id').text = ws.cell(row=cell.row,column=(cell.column + 2)).value
                SubElement(datum, 'Description').text = ws.cell(row=cell.row,column=(cell.column + 3)).value
                if ws.cell(row=cell.row,column=(cell.column + 4)).value is None:
                    SubElement(datum, 'HideFromUI').text = 'false'
                else:
                    SubElement(datum, 'HideFromUI').text = 'true'
                if ws.cell(row=cell.row,column=(cell.column + 5)).value is not None:
                    SubElement(datum, 'AttributeType').text = ws.cell(row=cell.row,column=(cell.column + 4)).value
                vals = SubElement(datum, 'Values')
                val = SubElement(vals, 'Value')
    return xml


def main():
    root = tk.Tk()
    root.withdraw()

    xlsx_path = None
    try:
        xlsx_path = filedialog.askopenfilename(parent=root, filetypes=[("template xlsx file", "template.xlsx")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    root.destroy()
    # create 2nd file till script is g2g
    if not xlsx_path:
        print('Must choose file path, quitting... ')
        quit()
    # Open Workbook
    wb = openpyxl.load_workbook(filename=xlsx_path, data_only=True)

    # Get All Sheets
    a_sheet_names = wb.sheetnames
    metadata_sheet = wb.get_sheet_by_name(name ="Metadata")
    # check for sheets
    if ('Metadata' and 'Threats' and 'Stencils') in a_sheet_names:
        print("All Sheets found!")
    else:
        print("Error! xlxs worksheets missing")
        quit()


    class XMLNamespaces:
        xsi = 'http://www.w3.org/2001/XMLSchema-instance'
        xsd = 'http://www.w3.org/2001/XMLSchema'

    root = Element(('KnowledgeBase'), nsmap={'xsi':XMLNamespaces.xsi, 'xsd':XMLNamespaces.xsd})

    # Add xml root's subelements
    # NOTE: Do not rename the worksheet default names or default title/tags for data (anything that's in bold font)
    root = get_manifest(root, metadata_sheet)
    root = get_Threat_Meta(root,metadata_sheet)
    GenericElements = SubElement(root, 'GenericElements')
    StandardElements = SubElement(root, 'StandardElements')
    root = get_threat_categories(root, metadata_sheet)
    ThreatTypes = SubElement(root, 'ThreatTypes')

    print('Finished!')
    # copy file and rename  extension
    tb7_path = os.path.splitext(xlsx_path)[0] + '.tb7'
    #TODO: remove once it's working
    tb7_path = tb7_path.replace('.tb7','2.tb7')
    outFile = open(tb7_path, 'wb')
    et = ElementTree(root)
    et.write(outFile, xml_declaration=True, encoding='utf-8', pretty_print=True) 

if __name__ == '__main__':
    main()
