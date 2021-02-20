# TMTool

A Threat Modeling GUI utility that works with Microsoft Threat Modeling Tool. This project aims to assist with the workfolw of template developers and model makers. For template design, this project hopes to address some of the complexities that come with managing a “database” of threats and stencils. For modeling, this project experiments with extracting metrics from our model and improving how Threat Modeling fits within DevOps/SDLC.

## Installation

```
$ pip install TMTool
```

## Usage

```
$ TMTool
```

## Scripts

.tb7 template files:

-	template2xlsx.py - enumerate a template's stencils, threat categories, and threats, and threat logic. Save elements/stencils and threats as a .xlsx file.

- xlsx2template.py - script to convert template.xlsx file back into a .tb7 file. For merging new threats or editing templates, you would modify and convert back to .tb7 format

- template2sql.py - enumerate a template's threats and stencils/elements. Save as SQLite .db file.


.tm7 model files:
-	set_metadata_tags.py - sets a model's metadata, such as risk level and compliance standards, in a Note entry
-	model_score.py (work in progress) - enumerate a model's notes, stencils, stencil properties (model metrics which we cannot get from TMT's built-in csv file generation). Then sets CVSS threat properties based on found element properties.
- cvss.py - script for scoring with CVSS v2. Imports pre-score metrics as a Dictionary.

MS Threat Model generated .csv threat list files:
- jira_issues.py - experimental script to add generated threat list to Jira Project as a set of issues. Also sets issue priority level and issue description from the threat. See empty_creds.py accessing your JIRA. This script can set the issue status to the threat's status if the JIRA transitions are available.

  ![](https://github.com/tmart234/TMT/blob/main/README.assets/TMT_boards.png)

HTML report files:
- fix_report_hyperlinks.py - This script will fix report hyperlinks that are broken since MS TMT encodes HTML entities within their generated report

- confluence.py - Script will publish a HTML and .docx report to confluence as an attachment

View threat_modeling_notes.txt for more