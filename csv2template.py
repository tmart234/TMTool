## this script will elements.csv and threats.csv files and convert
## back to a .tb7 file

import xml.etree.ElementTree as ET
import csv
import tkinter as tk
from tkinter import filedialog
import shutil
import os

script_path = os.path.dirname(os.path.abspath(__file__))

root = tk.Tk()
root.withdraw()

elements_path = filedialog.askopenfilename(parent=root, filetypes=[("element csv file", "elements.csv")])

threats_path = filedialog.askopenfilename(parent=root, filetypes=[("threats csv file", "threats.csv")])

print('got paths')
