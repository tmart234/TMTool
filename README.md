# TMT
Microsoft Threat Modeling Tool python scripts to increase TMT’s utility for both template developers and model makers.

3 scripts for .tb7 template files:
-	template2csv.py - enumerate a template's elements, threat categories, and threats, and threat logic. Convert to .csv format.

-	diff 2 template .csv files (produced in previous script) for template devs to compare and possibly to partially integrate new threats into their template. Categories: Major: missing stencils, flows, or threats entirely Minor: modified threat definition, modified threat logic, modified flow & stencil properties

- csv2template.py - script to convert the template.csv back to a .tb7 file. Ideally for merging, you'd import new threats then modify the threat logic to fit your template with a find & replace in excel


2 scripts for .tm7 model files:
-	model2csv.py - enumerate extra information from a model which we cannot get from TMT's built-in csv threat file. ex: notes, custom properties. Keep as separate csv file in conjunction with the TMT produced csv file.

-	diff 2 TMT produced csv files, regardless of TMT’s numbering or the ordering, to compare and to partially integrate one model’s derived threats into another.


2nd phase & future work
-	goal is to utilize TMT's built-in .HTM reporting and threat auditing features... but with more usability.
- explore scripts for validating templates by writing test models for a template's threats and parsing
-	Threat's Priority level should set from scoring (will need script for this, to figure out later. Will be a factor of severity and exploitability)
-	will need to set a Model’s risk threshold based on Priority levels (Ex: will only fix low-medium threats and up)
-	Threat Note entries are system/model level, not threat ID level like threat properties. Notes could contain system meta data for scripts.
