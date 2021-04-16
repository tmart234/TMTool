## this script will pull all threat categories, threats,
## and threat properties from a MS TMT template files (.tb7)
## and it will also pull all template's generic + standard elements
## after, it creates a template.xlsx file

import xlsxwriter
import xmltodict
from io import StringIO

from lxml import etree
import tkinter as tk
from tkinter import filedialog
import json
import os
import io
from shutil import copyfile

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
                elemnent_attribs = types.find('Attributes')
                self.attribs = etree.tostring(elemnent_attribs, encoding='utf-8', method='xml')
                # have to dump as json because we have an ordereddicts within ordereddicts
                self.attribs = json.loads(json.dumps(xmltodict.parse(self.attribs,process_namespaces=True,namespaces=namespaces)))
                self.attribs = str(self.attribs)

                my_list = [self.ele_name,ele_type,self.ele_id,self.ele_desc,self.ele_parent,self.hidden,self.rep, self.attribs]
                for col_num, data in enumerate(my_list):
                    stencil_worksheet.write(self.row, col_num, data)
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
    base = os.path.splitext(file_path)[0]
    wb_path = base + '.xlsx'
    
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
    threat_worksheet.write('A1', 'Threat Title', bold)
    threat_worksheet.write('B1', 'Category', bold)
    threat_worksheet.write('C1', 'ID', bold)
    threat_worksheet.write('D1', 'Description', bold)
    threat_worksheet.write('E1', 'Include Logic', bold)
    threat_worksheet.write('F1', 'Exclude Logic', bold)
    threat_worksheet.write('G1', 'Properties', bold)
    # start at row 1
    _row = 1
    for types in xml_root.iter('ThreatType'):
        # TODO: replace threat logic GUIDs with names in xlsx and make a guid lookup function for elements
        # get threat logic
        for gen_filters in types.findall('GenerationFilters'):
            for include_logic in gen_filters.findall('Include'):
                include = include_logic.text
            for exclude_logic in gen_filters.findall('Exclude'):
                exclude = exclude_logic.text
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
        # get all property data (all child elements)
        properties = types.find('PropertiesMetaData')
        prop_str = etree.tostring(properties, encoding='utf-8', method='xml')
        # have to dump as json because we have an ordereddicts within ordereddicts
        prop_str = json.loads(json.dumps(xmltodict.parse(prop_str,process_namespaces=True,namespaces=namespaces)))
        prop_str = str(prop_str)
        # TODO: get element constraints? 

        # WRITE EACH ROW ITERATIVELY 
        my_list = [title,category,threat_id,desc,include,exclude,prop_str]

        for col_num, data in enumerate(my_list):
            threat_worksheet.write(_row, col_num, data)
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