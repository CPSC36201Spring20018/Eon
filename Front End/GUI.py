# sys is needed to go back to parent directory
import sys
sys.path.append('../')
import controller as cont

# UI libs
from weather import Weather, Unit
import tkinter as tk                # python 3
from tkinter import ttk
from tkinter import font  as tkfont # python 3
from tkcalendar import Calendar, DateEntry
import datetime
import requests
import json

#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2


# TO DO:
# - change vacation label to be an airplane, red off green on

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        print('Starting up...')

        # Fonts defined here#
        self.temp_font = tkfont.Font(family= 'Calibri', size=40)
        self.time_font = tkfont.Font(family='Calibri', size=10)
        self.day_font = tkfont.Font(family='Calibri', size=15)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.title("Den")
        self.geometry("800x480")

        container = tk.Label(self)
        container.place(x=0, y=0, relwidth=1, relheight=1)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (StartPage, SettingsPage, CalendarPage):
            page_name = F.__name__

            frame = F(parent = container, controller=self)

            #spaceImage = tk.PhotoImage(file = "images/space.gif")
            #frame = tk.Label(self, image = spaceImage)
            #frame.image = spaceImage
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
            #frame.place(relx=0, rely=0)
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
            self.requestedtTempString = str(self.requestedTemperature)+"°F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.upButton.config(state="normal")
        else:
            self.downButton.config(state="disable")
        if not self.vacayIsOn:
            self.setRequestedTemperature() # uncomment to when connected to raspberry pi

    def tempUp(self):
        if(self.requestedTemperature < 90):
            self.requestedTemperature += 1
            self.requestedtTempString = str(self.requestedTemperature)+"°F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.downButton.config(state="normal")
        else:
            self.upButton.config(state="disable")

        if not self.vacayIsOn:
            self.setRequestedTemperature() # uncomment to when connected to raspberry pi


    def setRequestedTemperature(self):
        # check to see if system is on and update requestedTemperature
        if (self.isOn):
            # set system to requested temperature
            self.controll.setRequestedTemperature(self.requestedTemperature)

    # Custom timer without using any multithreading
    def starTimer(self):
        # timer should be called every 15 seconds
        self.timer(15)

    def timer(self,seconds):
        s = int(self.time)
        s += 1
        self.time = str(s)

        # keeps the gui from freezing
        self.after(930,self.starTimer)

        if(s == seconds):
            s = 0
            self.time = str(s)
            self.now = datetime.datetime.now().time()
            self.timeLabel.configure(text=self.now.strftime("%I:%M %p"))

            # check current indoor temperture
            self.controll.setCurrentTemperature()
            self.currentIndoorTempString = str(self.controll.getCurrentTemperature()) + "°F"
            self.currentIndoorTempLabel.configure(text=self.currentIndoorTempString)

            # check current outdoor temperture
            self.currentTempString = str(self.controll.getCityTemperature(self.variable.get())) + "°F"
            self.currentOutdoorTempLabel.configure(text=self.currentOutdoorTempString)

            if self.controll.getCurrentTemperature() <= self.controll.getRequestedTemperature() and self.controll.isAC():
                self.controll.deactivateAC()
            if self.controll.getCurrentTemperature() >= self.controll.getRequestedTemperature() and self.controll.isHeat():
                self.controll.deactivateHeat()
            if (self.controll.getCurrentTemperature() - self.controll.threshold > self.controll.getRequestedTemperature()) and not self.controll.isAC() and not self.vacayIsOn:
                if self.controll.isHeat():
                    self.controll.deactivateHeat()
                self.controll.activateAC()
            if self.controll.getCurrentTemperature() + self.controll.threshold < self.controll.getRequestedTemperature() and not self.controll.isHeat():
                if self.controll.isAC():
                    self.controll.deactivateAC()
                self.controll.activateHeat()


    def systemToggle(self):
        if(self.isOn == True):
            self.isOn = False
            powerImage = tk.PhotoImage(file = "images/powerOff.png")
            self.systemOnOffButton.configure(image = powerImage)
            self.systemOnOffButton.photo = powerImage
            self.systemOnOffButton.configure(text = "Off")
            self.controll.Disable()
        else:
            self.isOn = True
            powerImage = tk.PhotoImage(file = "images/powerOn.png")
            self.systemOnOffButton.configure(image = powerImage)
            self.systemOnOffButton.photo = powerImage
            self.systemOnOffButton.configure(text = "On")
            self.controll.Enable()

        self.setRequestedTemperature() # uncomment to when connected to raspberry pi


    def vacayToggle(self):
        if(self.vacayIsOn == True):
            self.vacayIsOn = False
            vacayImage = tk.PhotoImage(file ="images/airplaneModeOff.png")
            self.vacayButton.configure(image = vacayImage)
            self.vacayButton.photo = vacayImage
            self.systemOnOffButton.configure(text = "Off")
            self.controll.setVacation()
            self.setRequestedTemperature()
        else:
            self.vacayIsOn = True
            self.systemOnOffButton.configure(text = "On")
            vacayImage = tk.PhotoImage(file ="images/airplaneModeOn.png")
            self.vacayButton.configure(image = vacayImage)
            self.vacayButton.photo = vacayImage
            self.controll.setVacation()


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.vacayIsOn = False
        self.isOn = True
        self.currentTemperature = 80
        self.requestedTemperature = 70
        backgroundImage = tk.PhotoImage(file = "images/bg.png")
        background = tk.Label(self, image = backgroundImage)
        background.place(x=0, y=0, relwidth=1, relheight=1)
        background.image = backgroundImage

        # Instance Of Controller class
        self.controll = cont.Controller();

        ################################
        #                              #
        #       TIME_WIFI_SYSTEM       #
        #           SETTINGS           #
        ################################

       	wifiImage = tk.PhotoImage(file = "images/wifi.png")

        wifiLabel = tk.Label(self, image = wifiImage, bg = 'black')
        wifiLabel.place(relx=0.95, rely = 0.01)
        wifiLabel.image = wifiImage

	# Current Time being display top right corner
        self.now = datetime.datetime.now().time()

        self.timeLabel = tk.Label(self, text=self.now.strftime("%I:%M %p"), font=controller.time_font, bg = 'black', fg = 'white')
        self.timeLabel.config(font = ("Calibri", 17))
        self.timeLabel.place(relx = 0.55,rely = 0.35)

        ################################
        #                              #
        #    VACATION_CITY_CALENDAR    #
        #           SETTINGS           #
        ################################

	# Current date that will also be used as a button
	# displayed top right corner, nect to time
        today = datetime.date.today()
        calButton = tk.Button(self, text = today.strftime("%A, %b %d, %Y"), bg = 'black', relief = 'flat', fg = 'white', highlightbackground = 'black', activebackground='#333333', activeforeground = 'white', command=lambda: controller.show_frame("CalendarPage"))
        calButton.config(font = ("Calibri", 20))
        calButton.place(relx=0.53,rely=0.25)

        ################################
        #                              #
        #           CONTROLS           #
        #           SETTINGS           #
        #                              #
        ################################

        # Power Button
        powerButton = tk.PhotoImage(file = "images/powerOn.png")
        self.systemOnOffButton = tk.Button(self, image = powerButton, relief = 'flat', command= self.systemToggle, bg = 'black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        self.systemOnOffButton.image = powerButton
        self.systemOnOffButton.place(relx=.05, rely = 0.01)

	# settings button
        settingsImage = tk.PhotoImage(file = "images/settings.png")
        settingsButton = tk.Button(self, image = settingsImage, relief= 'flat',command=lambda: controller.show_frame("SettingsPage"), bg ='black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        settingsButton.image = settingsImage
        settingsButton.place(relx=0.1, rely=0.01)

	# vacation button
        vacayImage = tk.PhotoImage(file = "images/airplaneModeOff.png")
        self.vacayButton = tk.Button(self, image = vacayImage, relief='flat',command=self.vacayToggle, bg = 'black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        self.vacayButton.image = vacayImage
        self.vacayButton.place(relx=0.15,rely=0.01)


        ################################
        #                              #
        #      TWO_DIFFERENT_WAYS      #
        #       TO_DISPLAY_CITY        #
        #                              #
        ################################

        # Function to that would change temperture label when city is change
        def selectCity(value):
            days = [None] * 4
            forecast = self.controll.getForecast(value)
            if not self.vacayIsOn:
                self.requestedTemperature = int(forecast[0].high)
                self.requestedTempLabel.configure(text = str(self.requestedTemperature) +"°F")

        self.variable = tk.StringVar(self)
        self.variable.set("City")

        cities = ["Los Angeles,CA", "Las Vegas,NV", "New York,NY","Miami,FL","SEOUL, South Korea","São Paulo, Brazil","Bombay, India", "JAKARTA, Indonesia","Karachi, Pakistan","MOSKVA (Moscow), Russia","Istanbul, Turkey"]

        cityOptions = tk.OptionMenu(self, self.variable,*cities ,command=selectCity)
        cityOptions.configure(fg = 'white', bg = 'black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white', relief ='flat')
        cityOptions["menu"].config(fg = 'white', bg = 'black', selectcolor = 'black',activebackground='#333333', activeforeground = 'white')
        cityOptions.place(relx=0.2,rely=0.02)

        ################################
        #                              #
        #        3 DAY FORECAST        #
        #           SETTINGS           #
        ################################


        # Get current location based off of IP address
        self.variable.set(self.controll.getLocation())

        # Uses weather API to get three day forecast
        # Will forecast next three days, not today's forecast
        days = [None] * 4
        temp = [None] * 4
        forecast = self.controll.getForecast(self.variable.get())

        # Strings for current tempertures
        self.controll.setCurrentTemperature()
        self.currentIndoorTempString = str(self.controll.getCurrentTemperature()) + "°F"
        self.currentOutdoorTempString = str(self.controll.getCityTemperature(self.variable.get())) + "°F"

        for i in range(0,4):
            days[i] = forecast[i].day
            temp[i] = forecast[i].high + "°F"


        weatherImageArray = [None] * 4
        for i in range(0,4):
            weatherImageSearch = forecast[i].text
            if weatherImageSearch == "Sunny":
                weatherImage = tk.PhotoImage(file = "images/sunny.png")
            elif weatherImageSearch == "Partly Cloudy":
                weatherImage = tk.PhotoImage(file = "images/partlyCloudy.png")
            elif weatherImageSearch == "Mostly Cloudy":
                weatherImage = tk.PhotoImage(file = "images/mostlyCloudy.png")
            elif weatherImageSearch == "Cloudy":
                weatherImage = tk.PhotoImage(file = "images/cloudy.png")
            elif weatherImageSearch == "Breezy":
                weatherImage = tk.PhotoImage(file = "images/wind.png")
            elif weatherImageSearch == "Windy":
                weatherImage = tk.PhotoImage(file = "images/windy.png")
            elif weatherImageSearch == "Rainy":
                weatherImage = tk.PhotoImage(file = "images/rain.png")
            else:
                weatherImage = None

            weatherLabel = tk.Label(self, image =  weatherImage, bg = 'black')
            weatherLabel.image =  weatherImage
            weatherImageArray[i] = weatherLabel

        day1String = tk.StringVar()
        day1String.set(days[1])
        day1HighTempString = tk.StringVar()
        day1HighTempString.set(temp[1])

        day2String = tk.StringVar()
        day2String.set(days[2])
        day2HighTempString = tk.StringVar()
        day2HighTempString.set(temp[2])

        day3String = tk.StringVar()
        day3String.set(days[3])
        day3HighTempString = tk.StringVar()
        day3HighTempString.set(temp[3])

        # Label for the three day forecast
        day1Label = tk.Label(self, text=day1String.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day1HighTempLabel = tk.Label(self, text=day1HighTempString.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day1HighTempLabel.place(relx=0.85, rely=0.65)
        day1Label.place(relx=0.55, rely=0.65)
        weatherImageArray[1].place(relx=0.725, rely=0.65)

        day2Label = tk.Label(self, text=day2String.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day2HighTempLabel = tk.Label(self, text=day2HighTempString.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day2HighTempLabel.place(relx =0.85, rely = 0.75)
        day2Label.place(relx=0.55, rely=0.75)
        weatherImageArray[2].place(relx=0.725, rely=0.75)

        day3Label = tk.Label(self, text=day3String.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day3HighTempLabel = tk.Label(self, text=day3HighTempString.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day3HighTempLabel.place(relx=0.85, rely=0.85)
        day3Label.place(relx=0.55, rely=0.85)
        weatherImageArray[3].place(relx=0.725, rely=0.85)


        ################################
        #                              #
        #         TEMPERATURE          #
        #           SETTINGS           #
        #                              #
        ################################

        # indoor temperature
        self.requestedtTempString = str(self.requestedTemperature)+"°F"
        self.requestedTempLabel = tk.Label(self, text=self.requestedtTempString, font=controller.temp_font, bg = 'black',fg = 'white')
        self.requestedTempLabel.place(relx=0.2, rely=0.3)

        currentTextLabel = tk.Label(self, text = 'Current',font = ("Calibri, 15"),bg = 'black',fg = 'white')
        currentTextLabel.place(relx=0.55, rely=0.45)
        self.currentIndoorTempLabel = tk.Label(self, text=self.currentIndoorTempString, font=controller.temp_font, bg = 'black',fg = 'white')
        self.currentIndoorTempLabel.config(font = ("Calibri", 17))
        self.currentIndoorTempLabel.place(relx=0.85, rely=0.45)

	    # outdoor temperature

        outdoorTextLabel = tk.Label(self, text = self.variable.get(),font = ("Calibri, 15"),bg = 'black',fg = 'white')
        outdoorTextLabel.place(relx=0.55, rely=0.55)
        self.currentOutdoorTempLabel = tk.Label(self, text=self.currentOutdoorTempString, font=controller.temp_font, bg = 'black',fg = 'white')
        self.currentOutdoorTempLabel.config(font = ("Calibri", 17))
        self.currentOutdoorTempLabel.place(relx=0.85, rely=0.55)
        weatherImageArray[0].place(relx=0.8, rely=0.55)



        ################################
        #                              #
        #     TEMPERTURE_BUTTONS       #
        #           SETTINGS           #
        #                              #
        ################################

        # Up and Down Arrows Images
        upArrow = tk.PhotoImage(file = "images/up.png")
        downArrow = tk.PhotoImage(file = "images/down.png")

        self.upButton = tk.Button(self, image = upArrow, relief = 'flat',command= self.tempUp, bg = 'black', highlightbackground = 'black', highlightcolor = 'black',activebackground='#333333', activeforeground = 'white')
        self.upButton.image = upArrow
        self.upButton.place(relx=0.09, rely =0.55)
        self.downButton = tk.Button(self, image = downArrow, relief = 'flat', command= self.tempDown, bg = 'black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        self.downButton.place(relx=0.35, rely=0.55)
        self.downButton.image = downArrow

        # Turn system of at startup
        self.systemToggle()

        # Timer needed to check time and current tempertures for both indoor and outdoor
        self.time = str(0)
        self.starTimer()

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

class CalendarPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))

        button.pack(padx = 10)
        def print_sel():
            print(cal.selection_get())
        now = datetime.datetime.now()
        cal = Calendar(self,font="Arial 14", selectmode='day',cursor="hand1", year=now.year, month=now.month, day=now.day)
        cal.pack(fill="both", expand=True)
        tk.Button(self, text="ok", command=print_sel).pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
