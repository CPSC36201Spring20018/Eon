from tkinter import *

import tkinter as tk
import subprocess

def connectToWifi():
    print ("Connected to WIFI...")

def disconnectFromWifi():
    print ("Disconneted from WIFI...")

def donothing():
    print ("This is something")

def tempUp():
    temperature = temperature + 1
    print (temperature)

def tempDown():
    temperature = temperature - 1
    print (temperature)

mainWindow = tk.Tk()
mainWindow.title("EON Thermostat")

image = PhotoImage(file = "space.gif")
upArrow = PhotoImage(file = "arrow_up.gif")
downArrow = PhotoImage(file = "arrow_down.gif")

background = Label(mainWindow, image = image)
background.place(x = 0, y = 0, relwidth = 1, relheight = 1)

# Set the frame of the gui to the size of the image
background.pack()

temperature = 45

tempString = StringVar()
tempString.set("90"+"F")

tempLabel = Label(mainWindow,background = "#4c4364",textvariable = tempString, font = ("Helvetica", 40, "bold"))
tempLabel.place(x = 680, y = 100)

tempUpBttn = tk.Button()
tempUpBttn.config(image = upArrow, command = tempUp)
tempUpBttn.place(x = 600, y = 250)

tempDownBttn = tk.Button()
tempDownBttn.config(image = downArrow, command = tempDown)
tempDownBttn.place(x = 600, y = 400)


bttn = tk.Button(mainWindow, text ="Connect To WIFI", command = connectToWifi)
bttn.place(x = 0, y = 0)

#Lb1 = Listbox(mainWindow)
#Lb1.insert(1, "Sunday")
#Lb1.insert(2, "Monday")
#Lb1.insert(3, "Tuesday")
#Lb1.insert(4, "Wednesday")
#Lb1.insert(5, "Thursday")
#Lb1.insert(6, "Friday")
#Lb1.insert(7, "Saturday")
#Lb1.place(x = 0, y = 0)


mainWindow.mainloop()
