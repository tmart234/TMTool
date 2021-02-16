# this script will fix URL hyperlinks within the MS TMT report
# really annoying we even have to do this, let me know if there's a workaround

import html
import tkinter as tk
from tkinter import filedialog
from html import *

def main():
    root = tk.Tk()
    root.withdraw()

    try:
        file_path = filedialog.askopenfilename(parent=root, filetypes=[("MS TMT Report", "*.htm")])
    except FileNotFoundError:
        print('Must choose file path, quitting... ')
        quit()
    if not file_path:
        print('Must choose file path, quitting... ')
        quit()

    with open(file_path, 'r+') as f:
        html_string = f.read()
        # do it 4 times because once is not enough
        html_string = html.unescape(html_string)
        html_string = html.unescape(html_string)
        html_string = html.unescape(html_string)
        html_string = html.unescape(html_string)
        f.seek(0)
        f.write(html_string)
        f.truncate()

if __name__ == '__main__':
   main()
