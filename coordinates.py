from tkinter import *
import tkinter as tk


screensizex = 1300
screensizey = 632
root = Tk ()
root.geometry ('%dx%d' % (screensizex,screensizey))
root.title ("Data Logger B17B")
root.config(background = "black")

parenttitle = Label (root, text = "", fg = "black", font = (None, 10), anchor = "e")
parenttitle.grid (row = 1, column = 2)
btnahu= Button(root, text="AHU", width=10, height=1, background="white",
                        command=lambda: raiseframe(ahuparent))
btnahu.grid(row=2, column=2)
btncoldstor = Button(root, text="COLD STORAGE", width=10, height=1, background="white",
                        command=lambda: raiseframe(coldstorparent))
btncoldstor.grid(row=3, column=2)
filename = PhotoImage(file='b17.png')

def raiseframe (frame) :
    frame.tkraise()
    if frame == ahuparent :
        parenttitle.configure(text="AHU")
    if frame == coldstorparent :
        parenttitle.configure(text="COLD STORAGE")

coldstorparent = Frame(root, relief=RIDGE)
coldstorparent.grid(row = 1,rowspan = 70, column = 1)
coldstorparent.config(background='black')
bgcoldstor = Label(coldstorparent,image=filename)
bgcoldstor.grid(row = 0, column = 0)
ahuparent = Frame(root, relief=RIDGE)
ahuparent.grid(row = 1,rowspan = 70, column = 1)
ahuparent.config(background='black')
bgahu = Label(ahuparent,image=filename)
bgahu.grid(row = 0, column = 0)

def getorigin(eventorigin):
      global x,y
      x = eventorigin.x
      y = eventorigin.y
      print(x,y)

root.bind("<Button 1>",getorigin)
root.mainloop ()