*This project is currently in beta and is highly unstable!*

# TMTool

A simple GUI utility that provides additional workflows for Microsoft's Threat Modeling Tool

## Installation

```
$ pip install TMTool
```

## Usage

```
$ TMTool
```



## Project Goals:

 - Improve upon Microsoft Threat Modeling Tool by providing a simple interface of supplemental workflows

    - It's NOT a goal of this project to create the "perfect" threat model/model template. There are plenty of other projects for templates and threat databases.

 - This project works heavily off of the concept of "scoring methodologies" (such as OWASP Risk Rating and CVSS v2)

     - How can we abstract and automate the scoring rubric (a manual process) and bring the threat's score into the model file as a threat property?
     - Risk = Impact * Likelihood; Each scoring methodology contains metrics that can be further categorized into either Impact or Likelihood based metrics
     - Because Microsoft's Threat Modeling tool uses STRIDE, it is "threat" or "attacker" centric it. TMTool believes a Model's Stencils or Threats can contain the Likelihood based metrics, but determining Impact takes additional insight into the assets at hand: What are we protecting? Therefore, we also aim to provide an "asset centric" method that describes assets in a repeatable way in order to derive these Impact metrics.

 - For template design, this project hopes to address some of the complexities that come with managing a “database” of threats and stencils.

     - Make mass edits to threat logic or any other threat/stencil properties from excel
     - For using completed templates (not starting from test_template.tm7), additional workflow to import (blank) Likelihood based scoring metrics as either threat/stencil properties (template dev would have to fill these in) 

 - For modeling, this project experiments with extracting metrics from our model and improving how Threat Modeling fits within DevOps and SDLC

     - ![](https://github.com/tmart234/TMT/blob/main/README.assets/TMT_boards.png)

    

View threat_modeling_notes.md for more

