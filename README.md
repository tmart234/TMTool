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



![](https://github.com/tmart234/TMT/blob/main/README.assets/TMTool.png)

## Project Goals:

 - This project works heavily off of the concept of "scoring methodologies" (such as OWASP Risk Rating and CVSS v2)
- Each scoring methodology contains metrics that can be further categorized into either Impact or Likelihood based metrics
     - ![](https://github.com/tmart234/TMT/blob/main/README.assets/risk_venn_diagram.png)
     - Because Microsoft's Threat Modeling tool uses STRIDE, it is "threat" and/or "attacker" centric it. TMTool believes a Model's Stencils or Threats can contain the Likelihood based metrics, but determining Impact takes additional insight into the assets at hand: What are we protecting? Therefore, we also aim to provide an "asset centric" method that describes assets in a repeatable way in order to derive these Impact metrics.
     - Abstract the scoring rubric entirely when dealing with the generated threat list
 - For template design, this project hopes to address some of the complexities that come with managing a “database” of threats and stencils.

 - For Dev-Ops, this project experiments with uploading the results of Threat Modeling to tools like Jira and Confluence

     - ![](https://github.com/tmart234/TMT/blob/main/README.assets/TMT_boards.png)

​    

View threat_modeling_notes.md for more

