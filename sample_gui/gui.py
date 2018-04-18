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
