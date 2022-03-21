*A scattered collection of my thoughts on threat modeling and TMTool and an ever evolving TODO list*

## Project Goals:

- Automate risk scoring for threat modeling
  - Improve the generated report
- Integrate threat modeling into dev-ops
- Easier methods to audit and edit the threat model template file so we have an evolving source of truth

### Modeling:

- model notes contain system metadata for scoring scripts and other variables that shouldn't change.
	- ex: CVSS environmental metrics like Security Requirements (based on risk level) or the Target Distribution (proportion of vulnerable systems)
- TODO: explore importing threats via free/open sourced vulnerability management platform

### Assets

Because Microsoft's Threat Modeling tool uses STRIDE, it is "attacker" centric. TMTool believes in a hybrid centric approach. A Model's Stencils or Threats can contain the Likelihood based metrics, but determining Impact takes additional insight into the assets at hand: What are we protecting? Therefore, we also aim to provide an "asset centric" method that describes assets in a repeatable way in order to derive these Impact metrics.

An asset should be in a Threat (ex: keys in a side channel attack) or within a flow (TODO: CIA_form.py). This step is essential deriving CVSS impact metrics (C.I.A. + severity).

- The asset form should include: severity metrics of the asset (Safety, financial, operational & privacy/legislation), and defined list of either consequences, cost, or loss factors of the asset, and asset weight
- list of asset Cost/loss factors are mapped to determine impacted CIA metrics. C.I.A. is also mapped to STRIDE (S->C(IA*), T->IA, R->C, I->C, D-> A, E->CIA) as such to decide which impact metrics to set (ex: there should only be an confidentiality impact if we are talking about an Information Disclosure threat)

### Analyzing & Auditing:

- CVSS threat properties can always be overridden in MS tool's Analysis Mode before and after scoring
- Microsoft's "Export to CSV" function doesn't get everything needed (like metrics within stencil properties), therefore we parse and edit the model file directly
  - (TODO) Scoring and CIA script should ignore any status set to: "not applicable"

### Scoring script

- Each scoring methodology contains metrics that can be further categorized into either Impact or Likelihood based metrics
- The threat's CVSS score will be mapped to the threat's ["priority" level]( https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-feature-overview#priority-change) in Threat properties
- Use CVSS v2 base metrics + environmental metrics for now and try other scoring methodologies later (TODO: owasp_rr.py and more)
  - Ideally risk rating methodologies would be plug-and-play
- CVSS Severity will be chosen from a worst case decision between asset severity and threat property severity.

### Reporting/Documenting

- All threat properties and model notes will show up in the HTML report!
  - scoring metrics that are element properties are first mapped to threat properties before scoring
- Improve TMT's built-in HTML reporting
  - because of MS TMT's HTML sanitizer, this project needs to decode the HTML elements (~4 times) back to usable links within the report document
  - TODO: filter selected compliance standards from metadata note
  - TODO: color code the priority levels in report
- How can we present results in a similar manner to that of static analysis programs as far as identified risk level and compliance?

### Template

- Answers: "what are we building?" and "what could go wrong?" (threat database)
- (TODO) Script to add risk metrics to stencil and threat properties
  - Do the risk metrics get added to model file or added to template file and then reapplied to model??
- in test_template.tm7, we've added the following as Threat Properties: C.I.A. metrics (CVSS base), Access complexity (base), severity (environmental), CVSS overall score, and HTML Compliance Tags
  - (TODO) severity is only metric that should be in both asset-centric and threat-centric; a likelihood metric and an impact metric. Meaning it should reside as a threat property and be derived from asset discovery then be a worst case decision.

  - PyTM has a good example of these metrics within a [database of threats](https://github.com/izar/pytm/blob/master/docs/threats.md) ... so does [threagile]( https://github.com/Threagile/threagile/tree/master/risks/built-in)

### Mitigations

- Answers: "what are we going to do about it?"
- Microsoft has a decent collection of [mitigations](https://docs.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-mitigations)
	- unfortunately these mitigations are not baked into the TMT in a meaningful way where we can derive them
	- maybe we can categorize this mitigation list further based on STRIDE's desired properties?
- will need to answer the final question after settling on a mitigation: "did we do a good enough job?". We can address that answer in Threat's Justification section? would imply a second analysis after deciding on a mitigation? does the JIRA script help answer the second analysis/review?
- (TODO) Create a Jira "Issue Type" named Requirements and upload the threat's mitigation to requirements
	-  link Jira Issues to requirements. both are linked/synced to threat IDs

## TMTool Scripts 

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

### Typical Threat Modeling process:

Scope -> Model -> Analyze - Mitigate -> Documents

### Definitions

- Elements/stencils: can be either a data store, data flow, process, external entity, or trust boundary
- Threat Property: metadata that can be set for every generated threat
- Element Property: metadata that can be set for every element
- Model Note entry: system level and could contain system metadata

### Idea: diffing scripts

- diff template produced .xlsx file and .tm7 file. All template diffing can almost entirely be pulled from xlsx2template.py
- diff Microsoft TMT produced .csv files

### Future Goals

- Switch to PyQT
- Auditing a template file threat logic
- Address and explore how templates and/or threat databases can provide different [data-flow diagram depth layers](https://docs.microsoft.com/en-us/learn/modules/tm-provide-context-with-the-right-depth-layer/)
  - Layer 0: major system parts. Layer 1: secondary system parts. Layer 2: system's sub-components. Layer 3: every process and low-level system subpart
  - how would each layer look different in enterprise, mobile, and IoT applications? Would this require different templates for different depth layers?

### Resources

Just getting Started?: Read [MS threat modeling security fundamentals](https://docs.microsoft.com/en-us/learn/paths/tm-threat-modeling-fundamentals/)
[Threat Modeling in SecDevOps](https://github.com/DinisCruz/Book_SecDevOps_Risk_Workflow/tree/master/content/2.Risk-workflow/Threat-Models)

