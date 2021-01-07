# TMT
Microsoft Threat Modeling Tool scripts

First step will be writing (4) python scripts in order to increase TMT’s utility for both template developers and model makers. Both MS TMT files are xml based so we will need to parse each file and we will also use .csv files, so a little parsing and outputting to those too. 

2 scripts for .tb7 template files:
- template2csv.py - enumerate a template's elements, threat categories, and threats. Convert to .csv format
- diff 2 template .csv files (produced in previous script) for template devs to compare and possibly to partially integrate new threats into their template. 
Categories: 
Major: missing stencils, flows, or threats entirely
Minor: modified threat definition, modified threat logic, modified flow & stencil properties

2 scripts for .tm7 model files:
- enumerate extra information from a model ex: notes, custom properties. Add into a model’s csv file (or separate csv file depending on structure)
- diff 2 TMT produced csv files, regardless of TMT’s numbering or the ordering, to compare and to partially integrate one model’s derived threats into another

Steps
- convert files to xml by renaming the extension
- may want to format the .tm7 xml files for reading

.tm7 xml notes
- <a:KeyValueOfguidanyType> to find the elements used in the model
	- within element find  <i:type="c:string">value</b:Value>  for custom names
	- get custom element properties selection from <b:SelectedIndex> and the <values> above

