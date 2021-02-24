## Steps: load the MS TMT produced .csv file and model file, find "interactor" flow for each threat,
## parse flow elements find elemnt properties, fill in AV and Auth as threat properties (from element properites),
## load metadata (notes) and threat props into cvss dicts, and score dicts w/ cvss.py
## TODO: this method currently involves setting CIA + severity (CVSS threat props) in analysis mode (solve w/ data classification)

from lxml import etree
import tkinter as tk
from tkinter import filedialog
import json

# checks element props for their selected index for a given <_name>
def get_metric(_props, _name):
    for prop in _props:
        for key,value in dict(prop).items():
            if key is 'PropName' and _name in value:
                index = int(prop.get('SelectedIndex'))
                return prop.get('PropValues')[index]
    return None

def get_element(_ele):
    # set up dictionaries
    # single element dict
    element = dict.fromkeys(['GenericTypeId','GUID','Name','SourceGuid','TargetGuid', 'AV', 'Auth'])
    # namespace for prop elements
    ele_namespace = {'b': 'http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase'}
    any_namespace = {'a': 'http://schemas.microsoft.com/2003/10/Serialization/Arrays'}
    # create a custom element properties dict
    ele_prop = dict.fromkeys(['PropName', 'PropGUID', 'PropValues', 'SelectedIndex'])
    ele_props = []
    # temp list of property values
    _values = []
                    # GUID also at this level
    for ele4 in _ele.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
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
        element['AV'] = get_metric(ele_props, 'access vector')
        element['Auth'] = get_metric(ele_props, 'has authentication')
        return element

def get_meta(root):
    # find all note elements
    _id = ''
    msgs = dict()
    for notes in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Notes'):
        for note in notes.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Note'):
            for id in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Id'):
                _id = id.text
            for message in note.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Message'):
                _message = message.text
            msgs[_id] = _message
    for key,value in msgs.items():
        if "METADATA:" in value:
            _meta = str(value).replace("METADATA:","").replace("\'", "\"")
            return dict(json.loads(_meta))
    return None


def get_flows(root):
    flows = dict()
    for child in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceList'):
        for drawing in child.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceModel'):
            # dont need borders currently
            # for borders in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Borders'):
            #     _id, ele = get_element(borders)
            #     elements[_id] = ele
            for lines in drawing.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Lines'):
                # this level enumerates a model's elements
                for line in lines.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfguidanyType'):
                # unlike stencils, flows have a source and target guids
                    ele = get_element(line)
                    #print(ele['properties'])
                    flows[ele.get('GUID')] = ele
            return flows
    return None

def set_TPs(root, flows):

    return


def main():
    root = tk.Tk()
    root.withdraw()
    # get model file
    try:
        file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS threat model files", "*.tm7")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    if not file_path:
        print('Must choose file path, quitting... ')
        quit()

    root.destroy()
    tree = etree.parse(file_path)
    root = tree.getroot()

    meta = get_meta(root)
    if not meta:
        print('No meta found, choosing defualts')

    flows = get_flows(root)
    print(flows)
    set_TPs(root, flows)


if __name__ == '__main__':
   main()

