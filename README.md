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



## Automated Cyber-Risk Scoring

- Parsing Element properties from a model: For example a flow could have "access vector" as an element prop. 
- Parsing Threat properties from a model: For example a threat have "access complexity" as a threat property.
- And adding a repeatable way to describe assets and apply those assets to a model’s flows or threats. This step being able to derive CIA, severity, and risk impact of the score.

![](https://github.com/tmart234/TMT/blob/main/README.assets/risk_venn_diagram.png)

## Dev-Ops Integration

This project experiments with uploading the MS Threat Modeling results to other tools. For Jira, we create a set of issues and set the issue's priority based on the threat ID's risk score. For Confluence, we just upload the generated HTML report to the platform.

![](https://github.com/tmart234/TMT/blob/main/README.assets/TMT_boards.png)





![](https://github.com/tmart234/TMT/blob/main/README.assets/TMTool.png)



​    

View threat_modeling_notes.md for more

