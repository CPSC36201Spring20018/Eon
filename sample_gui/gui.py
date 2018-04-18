import tkinter as tk                # python 3
from tkinter import *
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.temp_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.time_font = tkfont.Font(family='Helvetica', size=10)
        self.day_font = tkfont.Font(family='Helvetica', size=16)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, SettingsPage, CityPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

def tempDown(temp):
    temp -= 1
    # requestedTemperature = StartPage.requestedTemperature
    # requestedTemperature -=  1
    print(temp)
    # requestedtTempString = StringVar()
    # requestedtTempString.set(str(requestedtTemperature)+"°"+"F")

def tempUp(temp):
    temp += 1
   # requestedTemperature = StartPage.requestedTemperature
   # requestedTemperature +=  1
    print(temp)
   # requestedtTempString = StringVar()
   # requestedtTempString.set(str(requestedtTemperature)+"°"+"F")

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        wifiImage = PhotoImage(file = "wifi.gif")
        wifiLabel = tk.Label(self, image = wifiImage)
        wifiLabel.grid(row = 0,column = 0)

        timeLabel = tk.Label(self, text="12:00pm", font=controller.time_font)
        timeLabel.grid(row = 0, column = 1)

        onOffLabel = tk.Label(self, text="System Off", font=controller.time_font)
        onOffLabel.grid(row = 0, column = 2)

        vacayButton = tk.Button(self, text="Vaction Mode")
        vacayButton.grid(row = 0, column = 3)

        vacayButton = tk.Button(self, text="Choose City", command=lambda: controller.show_frame("CityPage"))
        vacayButton.grid(row = 0, column = 4)

        day1TempLabel = tk.Label(self, text="Sunday", font=controller.day_font)
        day1TempLabel.grid(row = 0, column = 5)

        day2TempLabel = tk.Label(self, text="Monday", font=controller.day_font)
        day2TempLabel.grid(row = 1, column = 5)

        day3TempLabel = tk.Label(self, text="Tuesday", font=controller.day_font)
        day3TempLabel.grid(row = 2, column = 5)

        currentTemperature = 80
        requestedTemperature = 75

        currentTempString = StringVar()
        currentTempString.set(str(currentTemperature)+"°"+"F")

        requestedtTempString = StringVar()
        requestedtTempString.set(str(requestedTemperature)+"°"+"F")


        currentTempLabel = tk.Label(self, text=currentTempString.get(), font=controller.temp_font)
        currentTempLabel.grid(row = 1, column = 0)

        requestedTempLabel = tk.Label(self, text=requestedtTempString.get(), font=controller.temp_font)
        requestedTempLabel.grid(row = 2, column = 0)

        systemOnOffButton = tk.Button(self, text="System On")
        systemOnOffButton.grid(row = 3, column = 0)

        settingsButton = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsPage"))
        settingsButton.grid(row = 4, column = 0)

        # Up and Down Arrows Images

        upArrow = tk.PhotoImage(file = "up_arrow.gif")
        downArrow = tk.PhotoImage(file = "down_arrow.gif")

        upButton = tk.Button(self, text="Settings", command= lambda: tempUp(requestedTemperature))
        upButton.grid(row = 3, column = 5)

        downButton = tk.Button(self, text="Settings", command= lambda: tempDown(requestedTemperature))
        downButton.grid(row = 4, column = 5)

        # def systemToggle():
        #    global isOn
        #    isOn = !isOn

class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is settings page!", font=controller.temp_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class CityPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is cities page!", font=controller.temp_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()


#from tkinter import *
#
#import tkinter as tk
#import subprocess
#
#def connectToWifi():
#    print ("Connected to WIFI...")
#
#def disconnectFromWifi():
#    print ("Disconneted from WIFI...")
#
#def donothing():
#    print ("This is something")
#
#def tempUp():
#    global temperature
#    temperature += 1
#    tempString.set(str(temperature)+"°"+"F")
#
#def tempDown():
#    global temperature
#    temperature -=  1
#    tempString.set(str(temperature)+"°"+"F")
#
#
#mainWindow = tk.Tk()
#mainWindow.title("EON Thermostat")
#
#image = PhotoImage(file = "space.gif")
#upArrow = PhotoImage(file = "arrow_up.gif")
#downArrow = PhotoImage(file = "arrow_down.gif")
#
#background = Label(mainWindow, image = image)
#background.place(x = 0, y = 0, relwidth = 1, relheight = 1)
#
## Set the frame of the gui to the size of the image
#background.pack()
#
#
#variable = StringVar(mainWindow)
#variable.set("City") # default value
#
#cityOptions = OptionMenu(mainWindow, variable, "Los Angeles", "Las Vegas", "New York","Miami")
#cityOptions.place(x = 400, y = 0)
#
#temperature = 45
#
#tempString = StringVar()
#tempString.set(str(temperature)+"°"+"F")
#
#tempLabel = Label(mainWindow,background = "#4c4364",textvariable = tempString, font = ("Helvetica", 40, "bold"))
#tempLabel.place(x = 680, y = 100)
#
#tempUpBttn = tk.Button()
#tempUpBttn.config(image = upArrow, command = tempUp)
#tempUpBttn.place(x = 600, y = 250)
#
#tempDownBttn = tk.Button()
#tempDownBttn.config(image = downArrow, command = tempDown)
#tempDownBttn.place(x = 600, y = 400)
#
#
#bttn = tk.Button(mainWindow, text ="Connect To WIFI", command = connectToWifi)
#bttn.place(x = 0, y = 0)
#
##Lb1 = Listbox(mainWindow)
##Lb1.insert(1, "Sunday")
##Lb1.insert(2, "Monday")
##Lb1.insert(3, "Tuesday")
##Lb1.insert(4, "Wednesday")
##Lb1.insert(5, "Thursday")
##Lb1.insert(6, "Friday")
##Lb1.insert(7, "Saturday")
##Lb1.place(x = 0, y = 0)
#
#
#mainWindow.mainloop()
