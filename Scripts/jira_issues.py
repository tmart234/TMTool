""" 
This scrit will import the TMT generated csv file's threat list
and add each threat to a Jira project as a set of issues.
in Projects/<proj_key>/Project settings/Issue types add <issue_type>
including standard fields such as priority, assignee, and lables
TODO: add functionality to see if issue being added already exists in JIRA
 """
from jira import JIRA
import tkinter as tk
from tkinter import filedialog
import csv

# create a creds file with values
import creds

root = tk.Tk()
root.withdraw()

threat_path = filedialog.askopenfilename(parent=root, filetypes=[("threat csv file", "*.csv")])

# Jira project constants (fill in)
proj_key = 'TMT'
# TODO: added code to automatically addded category to JIRA?
issue_type = 'ThreatModel'

def get_mulList(*args):
    return map(list,zip(*args))

def check_issue_type(jira, issue):
    try:
        type_found = jira.issue_type_by_name(issue)
        if str(type_found) == issue:
            return True
        else:
            return False
    except:
        print('issue type not found')
        return False

def check_proj(jira, proj):
    try:
        projects = list(jira.projects())
        for item in projects:
            if proj == str(item):
                return True
        return False
    except:
        print('project not found')
        return False

def main():
    options = {
    'server': creds.server
    }
    jira = JIRA(options, basic_auth=(creds.user,creds.api_key))
   
    csv_data = open(threat_path,'r')
    # creates a dictionary of lists from the TMT produced .csv threat file
    data = list(csv.reader(csv_data))
    threat_dict = dict(zip(data[0],get_mulList(*data[1:])))

    # check if issue type and project exists
    if check_issue_type(jira, issue_type) and check_proj(jira, proj_key):
        ids = threat_dict.get('Id')
        titles = threat_dict.get('Title')
        dis = threat_dict.get('Description')
        priorities = threat_dict.get('Priority')
        states = threat_dict.get('State')
        for i in range(len(ids)):
            new_issue = jira.create_issue(project=proj_key, summary=titles[i],
                            description=dis[i], issuetype={'name': issue_type},
                            assignee ={'id': creds.acct_id}, priority={'name': str(priorities[i]).capitalize()})            
            # TODO: find transistions and set issue's state
            transitions = jira.transitions(new_issue)
            print([(t['id'], t['name']) for t in transitions])

if __name__ == '__main__':
   main()
