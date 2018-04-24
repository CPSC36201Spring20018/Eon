##############################################
# Created on: 
# Written by: 
#
##############################################
import Temperature
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

################################
#                              #
#           START_PAGE         #
#                              #
################################

class StartPage(tk.Frame):

    def tempDown(self):
        if(self.requestedTemperature > 60):
            self.requestedTemperature -= 1
            self.requestedtTempString = str(self.requestedTemperature)+""+"F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.upButton.config(state="normal")
        else:
            self.downButton.config(state="disable")

    def tempUp(self):
        if(self.requestedTemperature < 90):
            self.requestedTemperature += 1
            self.requestedtTempString = str(self.requestedTemperature)+""+"F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.downButton.config(state="normal")
        else:
            self.upButton.config(state="disable")

    def systemToggle(self):
        if(self.isOn == True):
            self.isOn = False
            self.systemOnOffButton.configure(text = "Off")
            self.onOffLabel.configure(text = "System Off")
        else:
            self.isOn = True
            self.systemOnOffButton.configure(text = "On")
            self.onOffLabel.configure(text = "System On")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

       	wifiImage = PhotoImage(file = "wifi.gif")
	
        wifiLabel = tk.Label(self, image = wifiImage)
        wifiLabel.grid(row = 0,column = 1)
        wifiLabel.image = wifiImage


        timeLabel = tk.Label(self, text="12:00pm", font=controller.time_font)
        timeLabel.grid(row = 0, column = 1)

        self.onOffLabel = tk.Label(self, text="System Off", font=controller.time_font)
        self.onOffLabel.grid(row = 0, column = 2)

        vacayButton = tk.Button(self, text="Vaction Mode")
        vacayButton.grid(row = 0, column = 3)

        vacayButton = tk.Button(self, text="Choose City", command=lambda: controller.show_frame("CityPage"))
        vacayButton.grid(row = 0, column = 4)


        # 3 Day forecast

        day1 = "Sunday "
        day2 = "Monday "
        day3 = "Tuesday "

        day1Temp = 80
        day2Temp = 78
        day3Temp = 82

        day1TempString = StringVar()
        day1TempString.set(day1+str(day1Temp)+""+"F")

        day2TempString = StringVar()
        day2TempString.set(day2+str(day2Temp)+""+"F")

        day3TempString = StringVar()
        day3TempString.set(day3+str(day2Temp)+""+"F")

        day1TempLabel = tk.Label(self, text=day1TempString.get(), font=controller.day_font)
        day1TempLabel.grid(row = 0, column = 5)

        day2TempLabel = tk.Label(self, text=day2TempString.get(), font=controller.day_font)
        day2TempLabel.grid(row = 1, column = 5)

        day3TempLabel = tk.Label(self, text=day3TempString.get(), font=controller.day_font)
        day3TempLabel.grid(row = 2, column = 5)


        self.currentTemperature = 80
        self.requestedTemperature = 75

        self.currentTempString = str(self.currentTemperature)+""+"F"

        self.requestedtTempString = str(self.requestedTemperature)+""+"F"


        self.currentTempLabel = tk.Label(self, text=self.currentTempString, font=controller.temp_font)
        self.currentTempLabel.grid(row = 1, column = 0)

        self.requestedTempLabel = tk.Label(self, text=self.requestedtTempString, font=controller.temp_font)
        self.requestedTempLabel.grid(row = 2, column = 0)

        self.systemOnOffButton = tk.Button(self, text="Off",command= self.systemToggle)
        self.systemOnOffButton.grid(row = 3, column = 0)

        self.isOn = False

        settingsButton = tk.Button(self, text="Settings", command=lambda: controller.show_frame("SettingsPage"))
        settingsButton.grid(row = 4, column = 0)

        # Up and Down Arrows Images

        upArrow = tk.PhotoImage(file = "up_arrow.gif")
        downArrow = tk.PhotoImage(file = "down_arrow.gif")

        self.upButton = tk.Button(self, image = upArrow, command= self.tempUp)
        self.upButton.image = upArrow
        self.upButton.grid(row = 3, column = 5)
        self.downButton = tk.Button(self, image = downArrow, command= self.tempDown)
        self.downButton.grid(row = 4, column = 5)
        self.downButton.image = downArrow
	



###################################
#                                 #
#           SETTINGS_PAGE         #
#                                 #
###################################
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
        label.grid(row = 0, column = 0)

        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.grid(row = 1, column = 0)

        Lb1 = Listbox(self)
        Lb1.insert(1, "SEOUL, South Korea")
        Lb1.insert(2, "Sao Paulo, Brazil")
        Lb1.insert(3, "Bombay, India")
        Lb1.insert(4, "JAKARTA, Indonesia")
        Lb1.insert(5, "Karachi, Pakistan")
        Lb1.insert(6, "MOSKVA (Moscow), Russia")
        Lb1.insert(7, "Istanbul, Turkey")
        Lb1.insert(8, "SEOUL, South Korea")
        Lb1.insert(9, "Sao Paulo, Brazil")
        Lb1.insert(10, "Bombay, India")
        Lb1.insert(11, "JAKARTA, Indonesia")
        Lb1.insert(12, "Karachi, Pakistan")
        Lb1.insert(13, "MOSKVA (Moscow), Russia")
        Lb1.insert(14, "Istanbul, Turkey")
        Lb1.grid(row = 0, column = 1)

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
