""" 
This scrit will upload the HTML report to Confluence
https://confluence.atlassian.com/conf64/html-macro-936511039.html
 """

from atlassian import Confluence
import tkinter as tk
from tkinter import filedialog
# create a creds file with values
import creds


# Confluence project constants (fill in)
page_id = '98305'
page_key = 'TMT'

root = tk.Tk()
# hide root window
root.withdraw()
# get CSV
threat_path = filedialog.askopenfilename(parent=root, filetypes=[("html report", "*.htm")])

def main():
    confluence = Confluence(
    url=creds.server,
    username=creds.user,
    password=creds.api_key,
    cloud=True)

    # Get all spaces with provided limit
    # additional info, e.g. metadata, icon, description, homepage
    spaces = dict(confluence.get_all_spaces(start=0, limit=500, expand=None))
    print(spaces.get('results'))

if __name__ == '__main__':
   main()
