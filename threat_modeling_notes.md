*A collection of my thoughts on threat modeling and TMTool*



### Typical Threat Modeling process:

Scope -> Model -> Analyze - Mitigate -> Document

### TMTool process:

#### For Templates:

Create threats & stencils within the MS TMT editor -> merge other templates w/ logic within MS TMT editor options -> merge in cvss_props_blank.tm7 template with script -> set CVSS stencil & threat properties -> convert to excel file -> mass modify threat logic (or other values) -> convert back to template file

#### For Models:

Scope -> Model -> TMTool Set Metadata (model's risk level, target distribution) -> TMTool CIA form (describe model flows) -> TMTool Score Model -> Generate HTML report and .csv threat list -> TMTool Jira or report clean up scripts



### Modeling:

- model notes could contain system metadata for scripts and other variables that shouldn't change.
	- ex: CVSS environmental metrics like Security Requirements (based on risk level) or the Target Distribution (proportion of vulnerable systems)
- TODO: explore importing threats via free/open sourced vulnerability management platform

### Analyzing & Auditing:

- utilize TMT's built-in Analysis as much as possible
  - CVSS threat properties can always be overridden Analysis mode before scoring, setting and scoring should always be separate processes
- "Export to CSV" function doesn't get everything we need, therefore using the model XML file would be better
- when auditing the generated threat IDs, if a False positive is identified, set status to: "not applicable"
  - Scoring script should ignore these
- (TODO: CIA_form.py) Enumerate model's flows and set CIA + severity metrics for each flow with a GUI
  - with data classification of each flow+ the stride category we could infer CIA metrics, needs exploring

### Scoring script

- Use CVSS base metrics + environmental metrics as threat properties.

  -  This seems easier than other complex things like [OWASP Risk rating methodology](https://owasp.org/www-community/OWASP_Risk_Rating_Methodology)

- CVSS needs threshold

- The threat's CVSS score will be mapped to the threat's ["priority" level]( https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-feature-overview#priority-change) in Threat properties

	

### Reporting/Documenting

- All scoring metrics are threat properties or notes and therefore will show up in the HTML report!
  - scoring metrics that are element properties are mapped to threat properties before scoring
- Improve TMT's built-in HTML reporting
  - because of MS TMT's HTML sanitizer, we need to decode the HTML elements (~4 times) back to usable links within the report document
  - TODO: filter selected compliance standards from metadata note
  - TODO: color code the priority levels in report

### Template

- Answers: "what are we building?" and "what could go wrong?" (threat database)
- (TODO) Explore merging CVSS metrics from script (adds stencil and threat properties)
- in test_template.tm7, I've added the following as Threat Properties: C.I.A. metrics (CVSS base), Access complexity (base), severity (environmental), CVSS overall score, and HTML Compliance Tags
	- asses if we should pre-set Access Complexity, Severity, and  HTML Compliance Tags (threat properties) within our threat database
	- PyTM has a good example of these metrics within a [database of threats](https://github.com/izar/pytm/blob/master/docs/threats.md)
	- so does [threagile]( https://github.com/Threagile/threagile/tree/master/risks/built-in)
- Address and explore how templates and/or threat databases can provide different [data-flow diagram depth layers](https://docs.microsoft.com/en-us/learn/modules/tm-provide-context-with-the-right-depth-layer/)
	- Layer 0: major system parts. Layer 1: secondary system parts. Layer 2: system's sub-components. Layer 3: every process and low-level system subpart
	- how would each layer look different in enterprise, mobile, and IoT applications? Would this require different templates for different depth layers?

### Mitigations

- Answers: "what are we going to do about it?"
- Microsoft has a decent collection of [mitigations](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-mitigations)
	- unfortunately these mitigations are not baked into the TMT in a meaningful way where we can derive them
	- maybe we can categorize this mitigation list further based on STRIDE's desired properties?
- will need to answer the final question after settling on a mitigation: "did we do a good enough job?". We can address that answer in Threat's Justification section? would imply a second analysis after deciding on a mitigation? does the JIRA script help answer the second analysis/review?
- (TODO) Create a Jira "Issue Type" named Requirements and upload the threat's mitigation to requirements
	-  link Jira Issues to requirements. both are linked/synced to threat IDs

## Scripts

.tb7 template files:

-	template2xlsx.py - enumerate a template's stencils, threat categories, and threats, and threat logic. Save elements/stencils and threats as a .xlsx file.

-	xlsx2template.py - script to convert template.xlsx file back into a .tb7 file. For merging new threats or editing templates, you would modify and convert back to .tb7 format

-	template2sql.py - enumerate a template's threats and stencils/elements. Save as SQLite .db file.


.tm7 model files:

-	set_metadata_tags.py - sets a model's metadata, such as risk level and compliance standards, in a Note entry
-	model_score.py (work in progress) - enumerate a model's notes, stencils, stencil properties (model metrics which we cannot get from TMT's built-in csv file generation). Then sets CVSS threat properties based on found element properties.
-	cvss.py - script for scoring with CVSS v2. Imports pre-score metrics as a Dictionary.

MS Threat Model generated .csv threat list files:

- jira_issues.py - experimental script to add generated threat list to Jira Project as a set of issues. Also sets issue priority level and issue description from the threat. See empty_creds.py accessing your JIRA. This script can set the issue status to the threat's status if the JIRA transitions are available.

  ![](https://github.com/tmart234/TMT/blob/main/README.assets/TMT_boards.png)

HTML report files:

- fix_report_hyperlinks.py - This script will fix report hyperlinks that are broken since MS TMT encodes HTML entities within their generated report

- confluence.py - Script will publish a HTML and .docx report to confluence as an attachment

### Definitions

Elements/stencils: can be either a data store, data flow, process, external entity, or trust boundary
Threat Property: metadata that can be set for every generated threat
Element Property: metadata that can be set for every element
Model Note entry: system level and could contain system metadata

### Idea: diffing scripts

- diff template produced .xlsx file and .tm7 file. All template diffing can almost entirely be pulled from xlsx2template.py
- diff Microsoft TMT produced .csv files

### Resources

Just getting Started?: Read [MS threat modeling security fundamentals](https://docs.microsoft.com/en-us/learn/paths/tm-threat-modeling-fundamentals/)
[Threat Modeling in SecDevOps](https://github.com/DinisCruz/Book_SecDevOps_Risk_Workflow/tree/master/content/2.Risk-workflow/Threat-Models)



### Future Goals:

 - explore verifying (threat logic) and auditing a template file

