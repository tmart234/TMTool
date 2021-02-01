""" 
Work in progress!!!
fill in: 'api_key', 'user' (email), and 'server' address
This scrit will check the TMT generated csv file's threat list
against a Jira project. Cycle through each row, get fields, check status,
and make changes to JIRA issues.
 """
from jira import JIRA

# Jira project credentials (fill in)
api_key = ''
user = ''
server = ''

# Jira project constants (fill in)
proj_key = 'TMT'
issue_type = 'Bug'

def check_issue_type(issue):
    try:
        type_found = jira.issue_type_by_name(issue)
        if str(type_found) == issue:
            return True
        else:
            return False
    except:
        print('not found')
        return False

def check_proj(proj):
    try:
        projects = list(jira.projects())
        for item in projects:
            if proj == str(item):
                return True
        return False
    except:
        print('not found')
        return False


options = {
 'server': server
}
jira = JIRA(options, basic_auth=(user,api_key))

# check if issue type and project exists
if check_issue_type(issue_type) and check_proj(proj_key):
    new_issue = jira.create_issue(project=proj_key, summary='New issue from jira-python',
                            description='Look into this one', issuetype={'name': issue_type})

# TODO: assign to user
# TODO: import threat list, get status, create predictable Jira IDs, update issues