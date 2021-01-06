# TMT
Microsoft Threat Modeling Tool scripts

First step will be writing (4) python scripts in order to increase TMT’s utility for both template developers and model makers. Both MS TMT files are xml based so we will need to parse each file and we will also use .csv files, so a little parsing and outputting to those too. 

2 scripts for .tb7 template files:
- find and enumerate a template file’s threats. Convert xml threats to tree structure (XPath to GraphViz dot https://github.com/TomConlin/xpath2dot) and also convert xml into .csv format (“Pip install xmlutils”?)
- diff 2 template .csv files (produced in previous script) for template devs to compare and possibly to partially integrate new threats into their template. Categories: 
Major: missing stencils, flows, or threats entirely
Minor: modified threat definition, modified threat logic, modified flow & stencil properties

2 scripts for .tm7 model files:
- enumerate extra information from a model ex: notes, custom properties. Add into a model’s csv file (or separate csv file depending on structure)
- diff 2 TMT produced csv files, regardless of TMT’s numbering or the ordering, to compare and to partially integrate one model’s derived threats into another

