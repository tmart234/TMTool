import tkinter as tk
from TMTool.Scripts import template2xlsx
from TMTool.Scripts import xlsx2template

def open_script1():
    template2xlsx.main()
    print("executed template2xlsx")

def open_script2():
    xlsx2template.main()
    print("executed xlsx2template")


def main():
    root = tk.Tk()
    frame = tk.Frame(root)
    frame.pack()

    button1 = tk.Button(frame, 
                    text="template2xlsx", 
                    command=open_script1)
    button1.pack(side=tk.LEFT)
    button2 = tk.Button(frame,
                    text="xlsx2template",
                    command=open_script2)
    button2.pack(side=tk.LEFT)

    root.mainloop()


if __name__ == '__main__':
    main()