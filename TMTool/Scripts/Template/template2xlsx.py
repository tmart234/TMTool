## this script will pull all threat categories, threats,
## and threat properties from a MS TMT template files (.tb7)
## and it will also pull all template's generic + standard elements
## after, it creates a template.xlsx file

import xlsxwriter
import xmltodict

from lxml import etree
import tkinter as tk
from tkinter import filedialog

import json
import os
import io
import re

namespaces = {
        'http://www.w3.org/2001/XMLSchema-instance': None # skip this namespace
        }

# blocking
def close_wb(_wb):
    while True:
        try:
            _wb.close()
        except xlsxwriter.exceptions.FileCreateError as e:
            decision = input("Exception caught in workbook.close(): %s\n"
                                "Please close the file if it is open in Excel.\n"
                                "Try to write file again? [Y/n]: " % e)
            if decision != 'n':
                continue

        break

# pull all threat Categories and their GUIDs from the XML
def find_cats(root):
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

# returns GUID in string using regex
def getStrGUID(_s):
    guid = re.findall("[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", _s)
    if guid:
        return guid[0]
    else:
        # MS Azure template uses non-guid IDs with periods
        if ' ' not in _s and '.' in _s:
            return _s
        else:
            return None

# take in GUID and look up the element name
def getGUIDName(_root, ele_type, _guid):
    if _guid:
        for _type in _root.findall(ele_type):
            for types in _type.iter('ElementType'):
                for subelem in types.findall('ID'):
                    ele_id = subelem.text
                    if ele_id == _guid:
                        for subelem in types.findall('Name'):
                            return subelem.text
                    else:
                        continue
    return None

# take in GUID and look up the prop name in element attribs
def getGUIDProp(_root, ele_type, _guid):
    if _guid:
        for _type in _root.findall(ele_type):
            for types in _type.iter('ElementType'):
                for subelem in types.findall('Attributes'):
                    for subelem2 in subelem.findall('Attribute'):
                        for subelem3 in subelem2.findall('Name'):
                            prop_id = subelem3.text
                            if prop_id == _guid:
                                for d_name in subelem2.findall('DisplayName'):
                                    return d_name.text
                            else:
                                continue
    return None

# finds all items in single quotes, replace any GUIDs with names
def replaceSingleQuote(_root, txt):
    items = re.findall(r"'(.*?)'", txt, re.DOTALL)
    for item in items:
        guid = getStrGUID(item)
        if guid == None:
            continue
        else:
            name = getGUIDName(_root, "GenericElements", guid)
            if not name:
                name = getGUIDName(_root, "StandardElements", guid)
                if not name:
                    print("Error: element not found")
                    continue
            txt = txt.replace(item, name)
    return txt

# finds all props within elements and replaces guid with display name
def replaceProps(_root, txt):
    # the remaining guids should be prop guids
    guids = re.findall("[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}", txt)
    for guid in guids:
        prop_name = getGUIDProp(_root, "GenericElements", guid)
        if not prop_name:
            prop_name = getGUIDProp(_root, "StandardElements", guid)
            if not prop_name:    
                print("Error: element not found")
                continue
        txt = txt.replace(guid, prop_name)
    return txt

# checks if label is an existing header, adds it if not
# then writes the value to that column and row
def writeProp(label, val, _ws, row, headers):
    col = None
    if label not in headers:
        _ws.write(0, len(headers), label)
        headers.append(label)
    col = headers.index(label)
    _ws.write(row, col, val)
    return

# gets elements (stencils, flows, and boundarys)
class Elements():
    def __init__(self):
        self.row = 1
    def write_row(self, _root, ele_type, stencil_worksheet):
        for _type in _root.findall(ele_type):
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
                        # get all property data (all child elements)

                my_list = [self.ele_name,ele_type,self.ele_id,self.ele_desc,self.ele_parent,self.hidden,self.rep, self.attribs]
                for col_num, data in enumerate(my_list):
                    stencil_worksheet.write(self.row, col_num, data)

                # TODO: reimplement the way we print threat props for elemt attribs
                #for attribs in types.findall('Attributes'):
                self.row = self.row + 1
        return

def main():
    
    root = tk.Tk()
    root.withdraw()

    file_path = None
    try:
        file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS threat template files", "*.tb7")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    if not file_path:
        print('Must choose file path, quitting... ')
        quit()
    
    with io.open(file_path, 'r', encoding='utf-8') as f:
        tree = etree.parse(f)
    xml_root = tree.getroot()

    # copy file and rename  extension
    wb_path = os.path.splitext(file_path)[0]
    wb_path = wb_path + '.xlsx'
    
    # Create a workbook and add a worksheet.
    workbook = xlsxwriter.Workbook(wb_path)

    # Add a bold format to use to highlight cells.
    bold = workbook.add_format({'bold': 1})

    threat_worksheet = workbook.add_worksheet('Threats')
    stencil_worksheet = workbook.add_worksheet('Stencils')

    title = ''
    category = ''
    threat_id = ''
    desc = ''
    include = ''
    exclude = ''

    # write threat headers in xlsx worksheet
    threat_headers = ['Threat Title', 'Category', 'ID', 'Description', 'Include Logic', 'Exclude Logic']
    for col_num, data in enumerate(threat_headers):
        threat_worksheet.write(0, col_num, data)

    # start at row 1
    _row = 1
    for types in xml_root.iter('ThreatType'):
        # get threat's threat logic
        for gen_filters in types.findall('GenerationFilters'):
            for include_logic in gen_filters.findall('Include'):
                include = include_logic.text
                if include:
                    # replace threat logic GUIDs with names
                    # first replace GUIDs in single quotes
                    include = replaceSingleQuote(xml_root, include)
                    # then replace GUIDs that are prop names ex: "flow.<guid>"
                    include = replaceProps(xml_root, include)
            for exclude_logic in gen_filters.findall('Exclude'):
                exclude = exclude_logic.text
                if exclude:
                    exclude = replaceSingleQuote(xml_root, exclude_logic.text)
                    exclude = replaceProps(xml_root, exclude)
        # get elements
        for subelem in types.findall('Category'):
            category = str(cat2str(subelem.text, find_cats(xml_root)))
        for subelem in types.findall('Id'):
            threat_id = subelem.text
        for subelem in types.findall('ShortTitle'):
            # remove curley braces for xlsx output
            title = subelem.text
        for subelem in types.findall('Description'):
            desc = subelem.text
        # WRITE EACH ROW ITERATIVELY 
        my_list = [title,category,threat_id,desc,include,exclude]

        for col_num, data in enumerate(my_list):
            threat_worksheet.write(_row, col_num, data)

        # get all property data (all child elements)
        for props in types.findall('PropertiesMetaData'):
            for prop in props.findall('ThreatMetaDatum'):
                _label = None
                _val = None
                for label in prop.findall('Label'):
                    _label = label.text
                for values in prop.findall('Values'):
                    for val in values.findall('Value'):
                        _val = val.text
                if _label:
                    writeProp(_label, _val, threat_worksheet, _row, threat_headers)
        # increase row
        _row = _row + 1

    # Elements headders
    #stencil_worksheet.write(['Stencil Name', 'Type', 'ID', 'Description','Parent', 'Hidden_bool', 'Representation', 'Attributes'])
    stencil_worksheet.write('A1', 'Stencil Name', bold)
    stencil_worksheet.write('B1', 'Type', bold)
    stencil_worksheet.write('C1', 'ID', bold)
    stencil_worksheet.write('D1', 'Description', bold)
    stencil_worksheet.write('E1', 'Parent', bold)
    stencil_worksheet.write('F1', 'Hidden_bool', bold)
    stencil_worksheet.write('G1', 'Representation', bold)
    stencil_worksheet.write('H1', 'Attributes', bold)

    # write generic elements
    Ele = Elements()
    Ele.write_row(xml_root, "GenericElements", stencil_worksheet)
    Ele.write_row(xml_root, "StandardElements", stencil_worksheet)

    close_wb(workbook)
    return

if __name__ == '__main__':
    main()