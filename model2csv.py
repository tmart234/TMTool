## this script will....
##
## <a:KeyValueOfguidanyType> to find the elements used in the model
## within element find <i:type="c:string">value</b:Value> for custom names
## get custom element properties selection from <b:SelectedIndex> and the above

import xml.etree.ElementTree as ET
import csv
import fnmatch

tree = ET.parse('sample2.xml')
root = tree.getroot()

with open('model.csv', 'w', newline='') as r:
    writer = csv.writer(r)
    # write headders in csv file
    writer.writerow(['Flow','Name'])

    for child in root.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceList'):
        for ele in child.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}DrawingSurfaceModel'):
            for ele2 in ele.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model}Lines'):
                for ele3 in ele2.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfguidanyType'):
                    for ele4 in ele3.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Value'):
                        for ele5 in ele4.findall('{http://schemas.datacontract.org/2004/07/ThreatModeling.Model.Abstracts}Properties'):
                            for ele6 in ele5.iter():
                                print(ele6.tag)
                                print(ele6.text)
