""" 
This scrit will import the TMT generated csv file's threat list
and add each threat to a Jira project as a set of issues.
in Projects/<proj_key>/Project settings/Issue types add <issue_type>
including standard fields such as priority, assignee, and lables
TODO: add functionality to see if issue being added already exists in JIRA
https://atlassian-python-api.readthedocs.io/jira.html
 """

from jira import JIRA
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import csv

# create a creds file with values
from . import creds

# Jira project constants (fill in)
proj_key = creds.api_key
# TODO: added code to automatically addded category to JIRA?
issue_type = "type"

def includeThreatStatus():
    MsgBox = tk.messagebox.askyesno(title='Include Status?',message='Include the threat ID status (JIRA Issue types must be set up)')
    return MsgBox

def deleteMessage():
    MsgBox = tk.messagebox.askyesno(title='Delete old project threats?',message='WARNING: This option will delete all project threats. Please select no or refine the delete_issues() function',icon='warning')
    return MsgBox

# ask user delete old issues
def deleteOld(jira):
    if deleteMessage():
        if delete_issues(jira, proj_key):
            print('Deleted all issues!')
        else:
            print('Error deleting old issues, check project key')

def get_mulList(*args):
    return map(list,zip(*args))
    
# see if issue type exists
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
# see if project exists
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

# deletes all project issues, used to clean up
def delete_issues(jira, proj_key):
    search_str = str("project=" + proj_key)
    try:
        issues = jira.search_issues(search_str, startAt=0, maxResults=100, validate_query=True, fields=None, expand=None, json_result=None)
        for issue in issues:
            issue.delete()
        return True
    except:
        return False

# see if we can transition from list of availible transitions
def checkTransitions(jira, issue, state):
    transitions = jira.transitions(issue)
    # transistions availible in MS
    ms_trans = ['Mitigated', 'Not Started', 'Needs Investigation', 'Not Applicable']
    # transistions availible in jira
    jira_trans = []
    for t in transitions:
        jira_trans.append(t['name'])
    # find in both lists
    for trans1 in ms_trans:
        for trans2 in jira_trans:
            # found
            if state == trans2 and state == trans1:
                return True
    return False

# transistion issue to desired state
def set_transition(jira, issue, state):
    # get transition ID
    transition_id = None
    transitions = jira.transitions(issue)
    for t in transitions:
        if t['name'] == state:
            transition_id = t['id']
    if transition_id == None:
        print("error could not find transition id")
    jira.transition_issue(issue, transition_id)

def main():
    
    root = tk.Tk()
    # hide root window
    root.withdraw()
    # get CSV
    try:
        threat_path = filedialog.askopenfilename(parent=root, filetypes=[("threat csv file", "*.csv")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    if not threat_path:
        print('Must choose file path, quitting... ')
        quit()

    options = {
    'server': creds.server
    }
    jira = JIRA(options, basic_auth=(creds.user,creds.api_token))

    # ask user to delete old issues
    deleteOld(jira)
    # UI option to include the threat status
    include_status = includeThreatStatus()

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
            # find transistions and set issue's state
            if include_status and checkTransitions(jira, new_issue, states[i]):
                # make sure all transistions exist for issue
                set_transition(jira, new_issue, states[i])


if __name__ == '__main__':
   main()
