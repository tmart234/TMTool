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

Steps to run scripts
- convert files to xml by renaming the extension

Model XML file Notes
- <a:KeyValueOfguidanyType> to find the elements used in the model
	- within element find  <i:type="c:string">value</b:Value>  for custom names
	- get custom element properties selection from <b:SelectedIndex> and the <values> above
	
2nd phase
- goal is to utilize TMT's built-in reporting features but with more usability
- add "severity" as custom threat property to template
- add "mitigation(s)" as custom threat property to template
- For False positives: set status="not applicable" for the threat ID
- Justification column should hold justification for either the severity or flase positive, not mitigations
- Threat's Priority level should get set from scoring (will need script, to figure out later: a facor of severity + explotibility)
- Threat Note entries are system/model level, not threat ID level

