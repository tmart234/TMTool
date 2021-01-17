# TMT
Microsoft Threat Modeling Tool python scripts to increase TMT’s utility for both template developers and model makers.

scripts for .tb7 template files:
-	template2csv.py - enumerate a template's elements, threat categories, and threats, and threat logic. Save elements and threats as a csv file.

- csv2template.py - script to convert template.csv file back into a .tb7 file. For merging new threats or editing templates, you would modify the threat logic or any other values with a simple find & replace and then convert back to .tb7 format


scripts for .tm7 model files:
-	model2csv.py - enumerate a model's flows, notes, elements, element properties, and any other information from a model which we cannot get from TMT's built-in csv file generation but which will later be used in conjunction with the generated csv file.

View threat_modeling_notes.txt for more
