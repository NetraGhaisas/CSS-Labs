import tkinter as tk
from tkinter import ttk
# import numbercap

class CapGUI:
    def __init__(self):
        window = tk.Tk()
        window.title('Captcha GUI')
        window.geometry('350x200')

        content = ttk.Frame(window,padding=(15,15,15,15))
        content.grid(column=0,row=0)

        lb = ttk.Label(content,text="Enter numeric value of expression")
        lb.grid(column=0,row=0)

        text = ttk.Entry(content)
        text.grid(column=0,row=1)
        rel = ttk.Button(content,text="Refresh")
        rel.grid(column=1,row=1)

        submit = ttk.Button(content,text="Submit")
        submit.grid(column=0,row=2)

        window.mainloop()

CapGUI()