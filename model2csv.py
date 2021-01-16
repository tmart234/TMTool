## this script will parse a model's elements to a csv file
## right now the script only enumerates flows and elements but needs more work


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
# multiple elements, values are a list of element dicts of those types
elements = dict.fromkeys(['flows','stencils','boundarys','interactors'])
# singular element dict
element = dict.fromkeys(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid','EleProperties'])
# TODO: create custom element properties dict as this part will change
# from <b:SelectedIndex> and the properties above

def write_element(ele2):
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
            for source in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}TargetGuid'):
                element['TargetGuid'] = source.text
            for ele5 in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}Properties'):
                for ele6 in ele5.iter('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}anyType'):
                    for ele7 in ele6.iter():
                     # find element's the custom name ex: "HTTPS Device In"
                            if "c:string" in str(ele7.attrib) and (ele7.text and ele7.text != '0'):
                                element['Name'] = ele7.text
                                # write element to csv row
                                writer.writerow([element['GenericTypeId'], element['GUID'], element['Name'], element['SourceGuid'], element['TargetGuid']])


with open('model.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    # write headders in csv file

    for child in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceList'):
        for ele in child.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceModel'):
            for borders in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Borders'):
                # write element headders
                writer.writerow(['Elements'])
                writer.writerow(['GenericTypeId','GUID','Name'])
                write_element(borders)
            for lines in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Lines'):
                writer.writerow([''])
                writer.writerow(['Flows'])
                writer.writerow(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid'])
                write_element(lines)
               
    
# delete temp .xml file created
if os.path.exists(folder_path):
  os.remove(folder_path)
else:
  print("The temp file does not exist")
