## this script will parse a model's elements to a csv file
## the script enumerates element's names, IDs, source GUID and target GUID of flows, 
## all element properties, and all model notes

import xml.etree.ElementTree as ET
import csv
import os
import tkinter as tk
from tkinter import filedialog

def write_element(ele2, writer):
     # set up dictionaries
    # single element dict
    element = dict.fromkeys(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid', 'properties'])
    # namespace for prop elements
    ele_namespace = {'b': 'http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase'}
    any_namespace = {'a': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'}
    # create a custom element properties dict
    ele_prop = dict.fromkeys(['PropName', 'PropGUID', 'PropValues', 'SelectedIndex'])
    ele_props = []
    # temp list of property values
    _values = []

         # this level enumerates a model's elements
    for ele3 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfguidanyType'):
                        # GUID also at this level
        for ele4 in ele3.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
            # get GUID
            for guid in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}Guid'):
                element['GUID'] = guid.text
            for gen_type in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}GenericTypeId'):
                element['GenericTypeId'] = gen_type.text
            for source in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}SourceGuid'):
                element['SourceGuid'] = source.text
            for target in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}TargetGuid'):
                element['TargetGuid'] = target.text
            for props in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}Properties'):
                for types in props.findall('.//a:anyType', any_namespace):
                # get all child elements of anyType element, all properties located here
                    for dis_name in types.findall('.//b:DisplayName', ele_namespace):   
                        ele_prop['PropName'] = dis_name.text
                    for prop_guid in types.findall('.//b:Name', ele_namespace):   
                        if prop_guid.text:
                            ele_prop['PropGUID'] = prop_guid.text
                        else:
                            ele_prop['PropGUID'] = ''
                    selection = types.find('.//b:SelectedIndex', ele_namespace)   
                    if selection is None:
                        ele_prop['SelectedIndex'] = ''
                        # get all prop values
                        value = types.find('.//b:Value', ele_namespace)
                        # set values
                        if value.text is None:
                            _values.append('')
                        else:
                            _values.append(value.text)
                        # set custom element name 
                        if ele_prop['PropName'] == 'Name':
                            element['Name'] = value.text
                            ele_prop['PropValues'] = _values.copy()
                    else:
                        # get prop selection
                        ele_prop['SelectedIndex'] = selection.text
                        # get value list for selection
                        for values in types.findall('.//b:Value/*', ele_namespace):
                            _values.append(values.text)
                        ele_prop['PropValues'] = _values.copy()
                     # add prop to prop list
                    _values.clear()
                    ele_props.append(ele_prop.copy())
                    ele_prop.clear()
            # save prop list to element dict
            element['properties'] = ele_props
            # print(element['properties'])
            # write to csv
            writer.writerow([element['GenericTypeId'], element['GUID'], element['Name'], element['SourceGuid'], element['TargetGuid'], element['properties']])
            ele_props.clear()

def main():
    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS threat model files", "*.tm7")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    if not file_path:
        print('Must choose file path, quitting... ')
        quit()

    root.destroy()
    tree = ET.parse(file_path)
    root = tree.getroot()

    # remame extension
    base = os.path.splitext(file_path)[0]
    os.rename(file_path, base + '.csv')

    with open(file_path, 'w', newline='') as r:
        writer = csv.writer(r)
        for child in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceList'):
            for ele in child.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceModel'):
                for borders in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Borders'):
                    # write element headders
                    writer.writerow(['Stencils'])
                    writer.writerow(['GenericTypeId','GUID','Name', '', '', 'Element Properties'])
                    write_element(borders, writer)
                for lines in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Lines'):
                    # create a new line with same doc and write element headders
                    writer.writerow([''])
                    writer.writerow(['Flows'])
                    # unlike stencils, flows have a source and target guids
                    writer.writerow(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid', 'Element Properties'])
                    write_element(lines, writer)
        # write note headders
        writer.writerow([''])
        writer.writerow(['Notes'])
        writer.writerow(['ID','Message'])
        _id = ''
        _message = ''
        # find all note elements
        for notes in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Notes'):
            for note in notes.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Note'):
                for id in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Id'):
                    _id = id.text
                for message in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Message'):
                    _message = message.text
                writer.writerow([_id,_message])


if __name__ == '__main__':
   main()

