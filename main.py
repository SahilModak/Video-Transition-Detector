from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image
import sti as sti
import func as func
import numpy as np
import time

root = Tk()

flag = 0

def popup():
  lol = Tk()
  lol.withdraw()

  file_path = filedialog.askopenfilename()
  return file_path

def getFolderName():
  s=simpledialog.askstring("Input Folder Name", "Please enter a name for a temporary folder")
  return s

def quit_me():
  print("Exiting Now")
  func.deletefolder(f_name)
  root.quit()
  root.destroy()

def columnSTI():
  # change image on canvas
  imag = Image.open(f_name+"/columnSTI.png")
  width = imag.width
  height = imag.height
  canvas1.config(width=width, height=height)
  canvas1.itemconfig(image_id, image=photo1)

def rowSTI():
  # change image on canvas
  imag = Image.open(f_name+"/rowSTI.png")
  width = imag.width
  height = imag.height
  canvas1.config(width=width, height=height)
  canvas1.itemconfig(image_id, image=photo2)

def columnHistoSTI():
  # change image on canvas
  imag = Image.open(f_name+"/colHistoSTI.png")
  width = imag.width
  height = imag.height
  canvas1.config(width=width, height=height)
  canvas1.itemconfig(image_id, image=photo3)

def rowHistoSTI():
  # change image on canvas
  imag = Image.open(f_name+"/rowHistoSTI.png")
  width = imag.width
  height = imag.height
  canvas1.config(width=width, height=height)
  canvas1.itemconfig(image_id, image=photo4)

def popupalert(alert_msg):
  popup = Tk()
  popup.wm_title("!")
  msg = ttk.Label(popup, text=alert_msg)
  msg.pack(side="top", fill="x", pady=10)
  button1 = Button(popup, text="Okay", command = popup.destroy)
  button1.pack()


root.protocol("WM_DELETE_WINDOW", quit_me)

Title = Label(root, text="                                                                      Spatio-Temporal Image (STI) Builder                                                                    ",fg="white", bg="blue")
Title.grid(row=1, column=3, rowspan=1, columnspan=5)

Note1 = Label(root, text="***Video Processing may take some time. Please be patient.",fg="black")
Note1.grid(row=2, column=3, rowspan=1, columnspan=5)

Note4 = Label(root, text="***When STI's are created, buttons will appear below.",fg="black")
Note4.grid(row=3, column=3, rowspan=1, columnspan=5)

#Setting up Canvas with Background Image
bg = PhotoImage(file="bg.png")
canvas1 = Canvas(width=500, height=500, bg = "grey")
canvas1.grid(row=8, column=3, rowspan=3, columnspan=5)
label = Label(root, image=bg)
image_id = canvas1.create_image(0,0,image=bg, anchor=NW)

Note2 = Label(root, text="CMPT 365 | Spring 2020 | Term Project",fg="black")
Note2.grid(row=12, column=3, rowspan=1, columnspan=5)

Note3 = Label(root, text="Sahil Modak | Ali Nanji",fg="black")
Note3.grid(row=13, column=3, rowspan=1, columnspan=5)



f_name = getFolderName()
if (f_name == None):
  alert_msg = "A Temporary Folder Name was not entered, 'tmp' will be used."
  popupalert(alert_msg)
  f_name = "tmp"



fileName = popup()
if (fileName == ""):
  sys.exit()

  

#Extracting Frames from Provided Video
numOfFrames = func.extractframes(fileName, f_name)

#Creating Row STI Image
tmp_array1 = sti.makeRowSTI(numOfFrames,f_name)
rowSTI_img=Image.fromarray(tmp_array1)
rowSTI_img.save(f_name+"/rowSTI.png")

#Creating Column STI Image
tmp_array2 = sti.makeColSTI(numOfFrames,f_name)
columnSTI_img=Image.fromarray(tmp_array2)
columnSTI_img.save(f_name+"/columnSTI.png")

#Creating Column Histogram STI Image
tmp_array3 = sti.createThresholdSTI(sti.makeColHistoIntersection(numOfFrames,f_name))
colHistoSTI_img=Image.fromarray((tmp_array3 * 255).astype(np.uint8))
colHistoSTI_img.save(f_name+"/colHistoSTI.png")

#Creating Row Histogram STI Image
tmp_array4 = sti.createThresholdSTI(sti.makeRowHistoIntersection(numOfFrames,f_name))
rowHistoSTI_img=Image.fromarray((tmp_array4 * 255).astype(np.uint8))
rowHistoSTI_img.save(f_name+"/rowHistoSTI.png")


photo1= PhotoImage(file=f_name+"/columnSTI.png")
photo2= PhotoImage(file=f_name+"/rowSTI.png")
photo3= PhotoImage(file=f_name+"/colHistoSTI.png")
photo4= PhotoImage(file=f_name+"/rowHistoSTI.png")

button_columnSTI = Button(root, text="Column STI", command=columnSTI)
button_columnSTI.grid(column=3, row=7)

button_rowSTI = Button(root, text="Row STI", command=rowSTI)
button_rowSTI.grid(column=4, row=7)

button_columnHistoSTI = Button(root, text="Column Histogram STI", command=columnHistoSTI)
button_columnHistoSTI.grid(column=5, row=7)

button_rowHistoSTI = Button(root, text="Row Histogram STI", command=rowHistoSTI)
button_rowHistoSTI.grid(column=6, row=7)




root.mainloop()