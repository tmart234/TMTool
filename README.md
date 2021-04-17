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

- Parsing Threat element properties from a model: For example flows could have "access vector" set as an element prop. 
- Next parsing Threat properties from a model: For example you could have "access complexity" set as a threat prop.
- Then adding a repeatable way to describe assets and apply those assets to a model’s flows in a repeatable way. This step mostly being able to derive CIA of the score.

![](https://github.com/tmart234/TMT/blob/main/README.assets/risk_venn_diagram.png)

## Dev-Ops Integration

This project experiments with uploading the MS Threat Modeling results to other tools. For Jira, we create a set of issues and set the issue's priority based on the threat ID's risk score. For Confluence, we just upload the generated HTML report to the platform.

- ![](https://github.com/tmart234/TMT/blob/main/README.assets/TMT_boards.png)





![](https://github.com/tmart234/TMT/blob/main/README.assets/TMTool.png)



​    

View threat_modeling_notes.md for more

