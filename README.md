# TMT
Microsoft Threat Modeling Tool python scripts to increase TMT’s utility for both template developers and model makers. For template design, this project hopes to address some of the complexities that come with managing a “database” of threats and stencils. For modeling, this project experiments with extracting information from our model and improving on the overall process of Threat Modeling. 

Scripts for .tb7 template files:
-	template2csv.py - enumerate a template's stencils, threat categories, and threats, and threat logic. Save elements/stencils and threats as a csv file.

- csv2template.py (work in progress) - script to convert template.csv file back into a .tb7 file. For merging new threats or editing templates, you would modify and convert back to .tb7 format

- template2sql.py - enumerate a template's threats and stencils/elements. Save as sqlite db


Scripts for .tm7 model files:
-	model2csv.py - enumerate a model's flows, notes, stencils, stencil properties, and any other information from a model which we cannot get from TMT's built-in csv file generation but which will later be used in conjunction with the generated csv file.

- set_metadata_tags.py (work in progress) - set a model's metadata such as risk level and compliance standards

- cvss.py (work in progress) - expiremental script for scoring threat IDs with CVSS

Scripts for MS TMT generated .csv threat list files:
- jira_issues.py - expiremental script to add generated threat list to Jira Project as a set of issues. Also sets issue priority level and issue description from the threat. See empty_creds.py accessing your JIRA. This script can set the issue status to the threat's status if the JIRA transistions are available.

Scripts for .htm report files:
- fix_report_hyperlinks.py - This script will fix report hyperlinks that are broken since MS TMT encodes HTML entities within their generated report

- confluence.py (work in progress) - Script will publish a HTML report to confluence

View threat_modeling_notes.txt for more
