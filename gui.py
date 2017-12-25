#!/usr/bin/python3
from tkinter import *
from imageScrapper import scrap
from tkinter import filedialog
def clicked():
	url=entry_ln.get()
	path=filedialog.askdirectory(title="Download to")
	scrap(url,path)

root=Tk()
root.geometry("300x300")
Label(root, text="Enter URL:").grid(row=0, sticky=W)
entry_ln = Entry(root)
entry_ln.grid(row=0, column=1)
b_start = Button(root, text="start")
b_start.grid(row=7, column = 1)
b_start['command']=clicked
root.mainloop()
