import tkinter as tk
from tkinter import messagebox
from TMTool.Scripts import template2xlsx
from TMTool.Scripts import xlsx2template
from TMTool.Scripts import jira_issues
from TMTool.Scripts import fix_report_hyperlinks
from TMTool.Scripts import model2csv

def open_script1():
    try:
        template2xlsx.main()
        print("executed template2xlsx")
    except Exception as ex:
        messagebox.showerror("Error", str("Error script failed: " + str(ex)))
    return

def open_script2():
    try:
        xlsx2template.main()
        print("executed xlsx2template")
    except Exception as ex:
        messagebox.showerror("Error", str("Error script failed: " + str(ex)))
    return

def open_script3():
    try:
        jira_issues.main()
        print("executed jira_issues")
    except Exception as ex:
        messagebox.showerror("Error", str("Error script failed: " + str(ex)))
    return

def open_script4():
    try:
        fix_report_hyperlinks.main()
        print("executed fix_report_hyperlinks")
    except Exception as ex:
        messagebox.showerror("Error", str("Error script failed: " + str(ex)))
    return

def open_script5():
    try:
        model2csv.main()
        print("executed model2csv")
    except Exception as ex:
        messagebox.showerror("Error", str("Error script failed: " + str(ex)))
    return


def main():
    root = tk.Tk()
    root.title("TMTool GUI")
    frame = tk.Frame(root)
    frame.pack()

    # template scripts (green background)
    button1 = tk.Button(frame, 
                    text="template2xlsx", 
                    command=open_script1,
                    fg = "white",
                    bg="green")
    button1.pack(side=tk.LEFT)
    button2 = tk.Button(frame,
                    text="xlsx2template",
                    command=open_script2,
                    fg = "white",
                    bg="green")
    button2.pack(side=tk.LEFT)

    # model scripts (blue)
    button3 = tk.Button(frame,
                    text="upload jira issues",
                    command=open_script3,
                    fg = "white",
                    bg="blue")
    button3.pack(side=tk.RIGHT)
    button4 = tk.Button(frame,
                    text="fix report hyperlinks",
                    command=open_script4,
                    fg = "white",
                    bg="blue")
    button4.pack(side=tk.RIGHT)
    button5 = tk.Button(frame,
                    text="model2csv",
                    command=open_script5,
                    fg = "white",
                    bg="blue")
    button5.pack(side=tk.BOTTOM)
    root.mainloop()


if __name__ == '__main__':
    main()