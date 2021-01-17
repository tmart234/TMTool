## this script will parse a model's elements to a csv file
## right now the script only enumerates element prop_names, IDs, source GUID and target GUID of flows
## also prints all element properties


import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog
import shutil
import os

script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS threat model files", "*.tm7")])
# copy and rename file extension
folder_path = os.path.join(script_path, "temp_model.xml")
shutil.copy(file_path, folder_path)

tree = ET.parse(folder_path)
root = tree.getroot()

# set up dictionaries
# singul element dict
element = dict.fromkeys(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid', 'properties'])
# namespace for prop elements
ele_namespace = {'b': 'http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase'}
any_namespace = {'a': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'}

def write_element(ele2):
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
            print(element['properties'])
            ele_props.clear()
            # write to csv
            writer.writerow([element['GenericTypeId'], element['GUID'], element['Name'], element['SourceGuid'], element['TargetGuid']])
    # if len(prop_guid_list) != len(prop_names):
    #     print ("prop list error")m
    #     print(len(prop_guid_list),len(prop_names))
    #     return
    # else:
    #     # print(prop_index)
    #     # print(prop_guid_list)
    #     # print(prop_names)
    #     for s in prop_values:
    #         print(*s)

with open('model.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    for child in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceList'):
        for ele in child.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceModel'):
            for borders in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Borders'):
                # write element headders
                writer.writerow(['Stencils'])
                writer.writerow(['GenericTypeId','GUID','Name'])
                write_element(borders)
            for lines in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Lines'):
                # create a new line with same doc and write element headders
                writer.writerow([''])
                writer.writerow(['Flows'])
                # unlike stencils, flows have a source and target guids
                writer.writerow(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid'])
                write_element(lines)
               
    
# delete temp .xml file created
if os.path.exists(folder_path):
  os.remove(folder_path)
else:
  print("The temp file does not exist")
