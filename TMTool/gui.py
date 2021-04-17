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

root = Tk()

def open_script1():
    template2xlsx.main()
    print("executed template2xlsx")
    root.destroy()
    return

def open_script2():
    xlsx2template.main()
    print("executed xlsx2template")
    root.destroy()
    return

def open_script3():
    jira_issues.main()
    print("executed jira_issues")

def open_script4():
    fix_report_hyperlinks.main()
    print("executed fix_report_hyperlinks")

def open_script5(root):
    root.destroy()
    set_metadata_tags.main()
    # TODO: inspect block
    print("executed set_metadata_tags")


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

    # template scripts (green background)
    button1 = ttk.Button(window, 
                    text="template2xlsx", 
                    command=open_script1)

    button2 = ttk.Button(window,
                    text="xlsx2template",
                    command=open_script2)

    # model scripts (blue)
    button3 = ttk.Button(window,
                    text="Upload as jira issues",
                    command=open_script3)

    button4 = ttk.Button(window,
                    text="Fix report hyperlinks",
                    command=open_script4)

    button5 = ttk.Button(window,
                    text="Set Model metadata",
                    command= open_script5)

    # light green
    text1 = ttk.Label(window,
                    text="Template Scripts:", foreground='#CCFFCC')
    # light blue
    text2 = ttk.Label(window,
                    text="Model Scripts:", foreground='#CCE5FF')

    # configure columns
    window.columnconfigure(0, weight=1)
    window.columnconfigure(1, weight=1)
    # make buttons grow when window and cells grow  
    text1.grid(row=0, column=0, sticky=W+E)
    text2.grid(row=0, column=1, sticky=W+E)
    button1.grid(row=1, column=0, sticky=W+E)
    button2.grid(row=2, column=0, sticky=W+E)
    button3.grid(row=3, column=1, sticky=W+E)
    button4.grid(row=2, column=1, sticky=W+E)
    button5.grid(row=1, column=1, sticky=W+E)
    root.mainloop()
    quit()

if __name__ == '__main__':
    main()