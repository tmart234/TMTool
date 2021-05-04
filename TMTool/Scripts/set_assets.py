## Steps: load the model file, parse flow elements find elemnt properties,
## find the "interactor" flow for each threat, fill in AV and Auth as threat properties (from element properites),
## load metadata (notes) and threat props into cvss dicts
# TODO: score dicts w/ cvss.py
# TODO: get flow CIA + severity from CIA_form.py and set threat properties within this script

from lxml import etree
import tkinter as tk
from tkinter import filedialog
import json
from . import asset_form
from .Scoring import cvss


# checks element props for anything containing <_name>
# returns props selected index value
def get_metric(_props, _name):
    for prop in _props:
        for key,value in dict(prop).items():
            if key is 'PropName' and _name in value:
                index = int(prop.get('SelectedIndex'))
                return prop.get('PropValues')[index]
    return None

# returns element as dictionary
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
        # TODO: search metrics should be a list
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

# returns threat props as dict
def get_TPs(root):
    TPs = dict()
    for ele in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}KnowledgeBase'):
        for e2 in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}ThreatMetaData'):
            for e3 in e2.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}PropertiesMetaData'):
                for e4 in e3.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}ThreatMetaDatum'):
                    _id = ''
                    _label = ''
                    for e5 in e4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Id'):
                        _id = e5.text
                    for e5 in e4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Label'):
                        _label = e5.text
                    TPs[_id] = _label
    return TPs

# finds threat ineractor (flow) and fills in flow values (AV and auth)
def set_TPs(root, flows):
    TPs = get_TPs(root)
    TP_AV_id = ''
    TP_Auth_id = ''
    for key,value in TPs.items():
        if value == 'Access Vector':
            TP_AV_id = key 
        if value == 'Authentication':
            TP_Auth_id = key

    for ele in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}ThreatInstances//*//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
        _interaction = ''
        threat_id = ''
        for id in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Id'):
            threat_id = id.text
        for e2 in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Properties'):
            for ele2 in e2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfstringstring'):
                for ele3 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Key'):
                    if ele3.text == 'InteractionString':
                        for e in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
                            # get interactor
                            _interaction = e.text
                            set_TP(root, flow_val(flows, 'AV', _interaction), threat_id, TP_AV_id)
                            set_TP(root, flow_val(flows, 'Auth', _interaction), threat_id, TP_Auth_id)
    return

# set a single threat prop <TP_id> to <_val>
def set_TP(root, _val, _id, TP_id):
    for ele in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}ThreatInstances//*//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
        for id in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Id'):
            if _id == id.text:
                for e2 in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Properties'):
                    for ele2 in e2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfstringstring'):
                        for ele3 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Key'):
                            if ele3.text == TP_id:
                                for ele4 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
                                    # set element TP here
                                    ele4.text = _val
                                    print('set threat ID: ' + _id +  ' threat prop id: ' + TP_id +' to val: ' + _val) 
    return

# check flows dictionary for <_flow_name>
# return the value of the flow's dictionary key <_key>
def flow_val(_flows, _key, _flow_name):
    for item,value in _flows.items():
        if value.get('Name') == _flow_name:
            return value.get(_key)
    print(_key +' Not found for ' + _flow_name)
    return None

# sees if current TP is a CVSS metric, return CVSS key or None
def check_TP(_TPs, _guid):
    my_list = ['Confidentiality','Integrity','Availability','Access Complexity','Access Vector','Authentication','Severity']
    for key,val in _TPs.items():
        for i, j in enumerate(my_list):
            if j == val:
                m = my_list[i]
                if m is 'Confidentiality':
                    return 'C'
                elif m is 'Integrity':
                    return 'I'
                elif m is 'Availability':
                    return 'A'
                elif m is 'Access Complexity':
                    return 'AC'
                elif m is 'Access Vector':
                    return 'AV'
                elif m is 'Authentication':
                    return 'Au'
                elif m is 'Severity':
                    return 'CDP'
                else:
                    print('error getting ' + val)
                    return None
            else:
                continue
    return None

# goes through threat ids, collects cvss data
def score_threats(root, meta):
    TPs = get_TPs(root)
    for ele in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}ThreatInstances//*//{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
        cvss_dict = dict.fromkeys('ID','AV','AC','Au','C','I','A','CDP','TD','CR','IR','AR')
        # set metrics from notes
        cvss_dict['TD'] = meta.get('TD')
        cvss_dict['CR'] = meta.get('CR')
        cvss_dict['IR'] = meta.get('IR')
        cvss_dict['AR'] = meta.get('AR')
        for id in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Id'):
            cvss_dict['ID'] = id.text
        for e2 in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.KnowledgeBase}Properties'):
            for ele2 in e2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfstringstring'):
                for ele3 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Key'):
                    _key = check_TP(TPs, ele3.text)
                    # not a CVSS metric
                    if not _key:
                        continue
                    else:
                        for ele4 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
                            cvss_dict[_key] = ele4.text
        score = cvss.CVSS(cvss_dict)
        print('scored threat ID ' + cvss_dict['ID'] + ' with a score of ' + score.overall_score)
        # TODO: set CVSS score string

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

    flows = asset_form.main(get_flows(root))
    print(flows)
    # set_TPs(root, flows)
    # score_threats(root, meta)

    # print('Finished!')
    # tree.write(file_path)

if __name__ == '__main__':
   main()

