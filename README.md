# TMT
Microsoft Threat Modeling Tool python scripts to increase TMT’s utility for both template developers and model makers. For template design, this project hopes to address some of the complexities that come with managing a “database” of threats and model elements. For modeling, this project experiments with extracting information from our model and improving on the overall process of Threat Modeling. 

scripts for .tb7 template files:
-	template2csv.py - enumerate a template's elements, threat categories, and threats, and threat logic. Save elements and threats as a csv file.

- csv2template.py (work in progress) - script to convert template.csv file back into a .tb7 file. For merging new threats or editing templates, you would modify the threat logic or any other values with a simple find & replace and then convert back to .tb7 format


scripts for .tm7 model files:
-	model2csv.py - enumerate a model's flows, notes, elements, element properties, and any other information from a model which we cannot get from TMT's built-in csv file generation but which will later be used in conjunction with the generated csv file.

- cvss.py (work in progress) - expiremental script for scoring threat IDs with CVSS

- jira_issues.py (work in progress) - expiremental script to add generated threat list file to Jira Project as a set of issues

View threat_modeling_notes.txt for more
