# TMT
Microsoft Threat Modeling Tool scripts

First step will be writing (4) python scripts to increase TMT’s utility for both template developers and model makers.

2 scripts for .tb7 template files:
-	template2csv.py - enumerate a template's elements, threat categories, and threats. Convert to .csv format.

-	diff 2 template .csv files (produced in previous script) for template devs to compare and possibly to partially integrate new threats into their template. Categories: Major: missing stencils, flows, or threats entirely Minor: modified threat definition, modified threat logic, modified flow & stencil properties


2 scripts for .tm7 model files:
-	model2csv.py - enumerate extra information from a model which we cannot get from TMT's built-in csv threat file. ex: notes, custom properties. Keep as separate csv file in conjunction with the TMT produced csv file.

-	diff 2 TMT produced csv files, regardless of TMT’s numbering or the ordering, to compare and to partially integrate one model’s derived threats into another.


Steps to run scripts:
-	convert files to xml by renaming the extension.


2nd phase
-	goal is to utilize TMT's built-in reporting and threat auditing features... but with more usability.
-	add "severity" as custom threat property to a custom template
-	add "mitigation(s)" as custom threat property to template
-	For False positives: set status="not applicable" for the threat ID
-	Justification column should hold justification for either the severity level or false positive, not for mitigations
-	Threat's Priority level should be more granular and set from scoring (will need script for this, to figure out later. Will be a factor of severity and exploitability)
-	will need to set a Model’s risk threshold based on Priority levels (Ex: will only fix low-medium threats and up)
-	Threat Note entries are system/model level, not threat ID level. Could contain system meta data.
