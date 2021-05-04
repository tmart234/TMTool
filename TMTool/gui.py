from tkinter import ttk
# override the basic Tk widgets
from tkinter.ttk import *
from tkinter import *
from ttkthemes import ThemedStyle

from TMTool.Scripts.Template import template2xlsx
from TMTool.Scripts.Template import xlsx2template
from TMTool.Scripts import jira_issues
from TMTool.Scripts import fix_report_hyperlinks
from TMTool.Scripts import set_metadata_tags
from TMTool.Scripts import set_assets
from TMTool.Scripts import confluence

root = Tk()

def open_temp2xlsx():
    template2xlsx.main()
    print("executed template2xlsx")
    root.destroy()
    quit()

def open_xlsx2temp():
    xlsx2template.main()
    print("executed xlsx2template")
    root.destroy()
    return

def open_jira_upload():
    jira_issues.main()
    print("executed jira upload")

def open_report_fix():
    fix_report_hyperlinks.main()
    print("fix HTML report hyperlinks")

def open_metadata():
    set_metadata_tags.main()
    print("set Model's Environmental metrics")
    return

def open_assets():
    set_assets.main()
    print("set Model's Assets")
    return

def upload_confluence():
    confluence.main()
    print("set Model's Assets")
    return


def main():
    root.configure(background='#404040')
    root.title("TMTool GUI")
    root.geometry("400x200")
    # Setting Theme
    style = ThemedStyle(root)
    style.set_theme("equilux")

    # for the main area of the window
    window = ttk.Frame(root)
    window.pack(fill=X, side=TOP)

    # light green
    text1 = ttk.Label(window,
                    text="Template Scripts:", foreground='#CCFFCC')
    # light blue
    text2 = ttk.Label(window,
                    text="Model Scripts:", foreground='#CCE5FF')
    # light purple
    text3 = ttk.Label(window,
                    text="Report Scripts:", foreground='#CCAAFF')

    # template scripts
    button1 = ttk.Button(window, 
                    text="Template -> XLSX", 
                    command=open_temp2xlsx)

    button2 = ttk.Button(window,
                    text="XLSX -> Template",
                    command=open_xlsx2temp)
    
    # report Scripts
    button4 = ttk.Button(window,
                    text="Fix Report",
                    command=open_report_fix)

    # model scripts 
    button3 = ttk.Button(window,
                    text="Upload as Jira Issues",
                    command=open_jira_upload)

    button5 = ttk.Button(window,
                    text="Set Model Metadata",
                    command= open_metadata)

    button6 = ttk.Button(window,
                    text="Set Model Assets",
                    command= open_assets)

    button7 = ttk.Button(window,
                    text="Upload to Confluence",
                    command= upload_confluence)

    # configure columns
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    # make buttons grow when window and cells grow  
    text1.grid(row=0, column=0, sticky=W+E)
    text2.grid(row=0, column=1, sticky=W+E)
    button1.grid(row=1, column=0, sticky=W+E)
    button2.grid(row=2, column=0, sticky=W+E)
    text3.grid(row=3, column=0, sticky=W+E)
    button4.grid(row=4, column=0, sticky=W+E)
    button6.grid(row=1, column=1, sticky=W+E)
    button5.grid(row=2, column=1, sticky=W+E)
    button3.grid(row=3, column=1, sticky=W+E)
    button7.grid(row=4, column=1, sticky=W+E)
    root.mainloop()
    quit()

if __name__ == '__main__':
    main()