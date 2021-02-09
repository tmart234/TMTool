""" 
This scrit will upload the HTML and docx report to Confluence
It will create a parent page and put the report in a child page as attachments
https://confluence.atlassian.com/conf64/html-macro-936511039.html
# TODO: embed the report into the page's body
 """

import tkinter as tk
from tkinter import filedialog
# create a creds file with values
import creds
import datetime
import os

from atlassian import Confluence
import pypandoc

# Confluence project constants (fill in)
page_space = 'TMT'
parent_title = 'Threat Model Reports'

def get_space_id(conflu):
    for x in conflu:
        c = dict(x)
        if c.get('key') == page_space:
            return c.get('id') 
    else:
        return None

root = tk.Tk()
# hide root window
root.withdraw()
# get HTML
report_path = filedialog.askopenfilename(parent=root, filetypes=[("html report", "*.htm")])

# create page title based on date 
d = datetime.datetime.now()
page_title = str(os.path.split(report_path)[1])

def main():
    confluence = Confluence(
    url=creds.server,
    username=creds.user,
    password=creds.api_key,
    cloud=True)

    conflu = dict(confluence.get_all_spaces(start=0, limit=500, expand=None))
    conflu = list(conflu.get('results'))
    id = get_space_id(conflu)
    if id:
        #space_id = id
        _parent_id = confluence.get_page_id(space = page_space, title = parent_title)
        # create parent page if it does not exist
        if not _parent_id:
            confluence.create_page(space = page_space, title= parent_title, body='This is a parent page for all Threat model reprots')
            _parent_id = confluence.get_page_id(space=page_space, title=parent_title)
        # create page
        confluence.update_or_create(parent_id =_parent_id ,title = page_title, body = '')
        _page_id = confluence.get_page_id(space=page_space, title=page_title)

        pypandoc.convert_file(source_file=report_path, format='html', to='docx', outputfile='temp.docx', extra_args=['-RTS'])
        # attach both formats
        confluence.attach_file(filename='temp.docx', page_id=_page_id, title=page_title, space=page_space)
        confluence.attach_file(filename=report_path, page_id=_page_id, title=page_title, space=page_space)
    else:
        print('could not retrieve space_id')
        os._exit(os.EX_OK)

if __name__ == '__main__':
   main()
