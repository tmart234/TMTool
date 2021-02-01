""" 
Work in progress!!!
This scrit will check the TMT generated csv file's threat list
against a Jira project. Cycle through each threat ID, get its fields, check its status,
and make changes to JIRA issues accordingly
 """
from jira import JIRA
import tkinter as tk
from tkinter import filedialog
import csv

# create creds file with values
import creds

root = tk.Tk()
root.withdraw()

threat_path = filedialog.askopenfilename(parent=root, filetypes=[("threat csv file", "*.csv")])

# Jira project constants (fill in)
proj_key = 'TMT'
issue_type = 'Bug'

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

    # check if issue type and project exists
    if check_issue_type(jira, issue_type) and check_proj(jira, proj_key):
        new_issue = jira.create_issue(project=proj_key, summary='New issue from jira-python',
                                description='Look into this one', issuetype={'name': issue_type},
                                assignee ={'id': creds.acct_id})

    # TODO: import threat list, get status, create predictable Jira IDs, update issues
    with open(threat_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

if __name__ == '__main__':
   main()
