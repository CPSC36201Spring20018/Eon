##############################################
# Created on: 
# Written by: 
#
##############################################
from weather import Weather, Unit
import tkinter as tk                # python 3
from tkinter import ttk
from tkinter import font  as tkfont # python 3
from sample_gui.tkcalendar import Calendar, DateEntry
import datetime
import requests
import json
import controller as cont

#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2


# TO DO:
# - change vacation label to be an airplane, red off green on

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
     
        # Fonts defined here#
        self.temp_font = tkfont.Font(family='Ariel', size=35, weight="bold", slant="italic")
        self.time_font = tkfont.Font(family='Ariel', size=10)
        self.day_font = tkfont.Font(family='Ariel', size=12)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        self.title("Den")
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        self.geometry("%dx%d+0+0"%(w,h))

 
        spaceImage = tk.PhotoImage(file = "space.gif")
        spaceLabel = tk.Label(self, image = spaceImage)
        spaceLabel.place(x=0, y=0, relwidth=1, relheight=1)
        spaceLabel.pack(side="top", fill="both", expand=True)
        spaceLabel.image = spaceImage
        
        spaceLabel.grid_rowconfigure(0, weight=1)
        spaceLabel.grid_columnconfigure(0, weight=1)


        self.frames = {}
        for F in (StartPage, SettingsPage, CityPage, CalendarPage):
            page_name = F.__name__
            frame = F(parent=spaceLabel, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            #frame.grid(row=0, column=0, sticky="nsew")
            frame.place(relx=0, rely=0)
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

    def tempUp(self):
        if(self.requestedTemperature < 90):
            self.requestedTemperature += 1
            self.requestedtTempString = str(self.requestedTemperature)+"°F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.downButton.config(state="normal")
        else:
            self.upButton.config(state="disable")

    def systemToggle(self):
        if(self.isOn == True):
            self.isOn = False
            self.systemOnOffButton.configure(text = "Off")
        else:
            self.isOn = True
            self.systemOnOffButton.configure(text = "On")

    def vacayToggle(self):
        if(self.vacayIsOn == True):
            self.vacayIsOn = False
            self.systemOnOffButton.configure(text = "Off")

        else:
            self.vacayIsOn = True
            self.systemOnOffButton.configure(text = "On")


    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.vacayIsOn = False
        self.isOn = False
        self.currentTemperature = 80
        self.requestedTemperature = 75
        
        controller = cont.Controller()
        
        ################################
        #                              #
        #       TIME_WIFI_SYSTEM       #
        #           SETTINGS           #
        ################################

       	wifiImage = tk.PhotoImage(file = "wifi.gif")
	
        wifiLabel = tk.Label(self, image = wifiImage)
        wifiLabel.place(relx=0.95, rely = 0.01)
        wifiLabel.image = wifiImage
        
	# Current Time being display top right corner
        now = datetime.datetime.now().time()

        timeLabel = tk.Label(self, text=now.strftime("%I:%M %p"), font=controller.time_font)
        timeLabel.place(relx = 0.8,rely = 0.01)
       
        ################################
        #                              #
        #    VACATION_CITY_CALENDAR    #
        #           SETTINGS           #
        ################################
  
	# Current date that will also be used as a button
	# displayed top right corner, nect to time
        today = datetime.date.today()
        calButton = tk.Button(self, text = today.strftime("%m/%d/%y"),relief = 'flat', command=lambda: controller.show_frame("CalendarPage"))

        calButton.place(relx=0.85,rely=0.001)

        ################################
        #                              #
        #           CONTROLS           #
        #           SETTINGS           #
        #                              #
        ################################

        self.systemOnOffButton = tk.Button(self, text="Off", command= self.systemToggle)
        self.systemOnOffButton.place(relx=0, rely = 0.01)
        settingsImage = tk.PhotoImage(file = "cog.png")
        
        settingsButton = tk.Button(self, image = settingsImage, relief= 'flat',command=lambda: controller.show_frame("SettingsPage"))
        settingsButton.image = settingsImage
        settingsButton.place(relx=0.05, rely=0.01)
        vacayButton = tk.Button(self, text="Vaction Mode", command=self.vacayToggle)
        vacayButton.place(relx=0.09,rely=0.01)


        ################################
        #                              #
        #      TWO_DIFFERENT_WAYS      #
        #       TO_DISPLAY_CITY        #
        #                              #
        ################################
        
        # Function to that would change temperture label when city is change
        def selectCity(value):
            days = [None] * 4
            forecast = controller.getForecast(value)
            for i in range(0,4):
                days[i] = forecast[i].day + " " + forecast[i].date + "\t\t" + forecast[i].high + "° F"
            day1TempLabel.configure(text = days[1])
            day2TempLabel.configure(text = days[2])
            day3TempLabel.configure(text = days[3])
    
        
        self.variable = tk.StringVar(self)
        self.variable.set("City")
        
        cities = ["Los Angeles,CA", "Las Vegas,NV", "New York,NY","Miami,FL","SEOUL, South Korea","São Paulo, Brazil","Bombay, India", "JAKARTA, Indonesia","Karachi, Pakistan","MOSKVA (Moscow), Russia","Istanbul, Turkey"]

        cityOptions = tk.OptionMenu(self, self.variable,*cities ,command=selectCity)
        cityOptions.place(relx=0.2,rely=0.01)
        
        # Trying to figure out how to pass data through pages
#        vacayButton = tk.Button(vccFrame, text="Choose City", command=lambda: controller.show_frame("CityPage"))
#        vacayButton.pack(side='left')


        ################################
        #                              #
        #        3 DAY FORECAST        #
        #           SETTINGS           #
        ################################

        # 3 Day forecast
        def threeDayForecast(loc):
            weather = Weather(unit=Unit.FAHRENHEIT)
            location = weather.lookup_by_location(loc)
            forecasts = location.forecast
            return forecasts
    
        def locationTemperature(loc):
            weather = Weather(unit=Unit.FAHRENHEIT)
            location = weather.lookup_by_location(loc)
            condition = location.condition
            temperature = condition.temp
            return temperature
        
        # Get current location based off of IP address
#        send_url = 'http://freegeoip.net/json'
#        r = requests.get(send_url)
#        j = json.loads(r.text)
#        city = j['city']
#        reg_code = j['region_code']
#        locat = city + ',' + reg_code
#        self.variable.set(locat)

        # Uses weather API to get three day forecast
        # Will forecast next three days, not today's forecast
        days = [None] * 4
        forecast = controller.getForecast(controller.getLocation())
        for i in range(1,4):
            days[i] = forecast[i].day + " " + forecast[i].date + "\t\t" + forecast[i].high + "°F"
        print(locat)
 
        day1TempString = tk.StringVar()
        day1TempString.set(days[1])

        day2TempString = tk.StringVar()
        day2TempString.set(days[2])

        day3TempString = tk.StringVar()
        day3TempString.set(days[3])

        # Label for the three day forecast
        day1TempLabel = tk.Label(self, text=day1TempString.get(), font=controller.day_font)
        day1TempLabel.place(relx=0.6, rely=0.3)

        day2TempLabel = tk.Label(self, text=day2TempString.get(), font=controller.day_font)
        day2TempLabel.place(relx=0.6, rely=0.4)

        day3TempLabel = tk.Label(self, text=day3TempString.get(), font=controller.day_font)
        day3TempLabel.place(relx=0.6, rely=0.5)


        ################################
        #                              #
        #         TEMPERATURE          #
        #           SETTINGS           #
        #                              #
        ################################


        self.currentTempString = str(self.currentTemperature)+"°F"
        self.requestedtTempString = str(self.requestedTemperature)+"°F"

        self.currentTempLabel = tk.Label(self, text=self.currentTempString, font=controller.temp_font)
        self.currentTempLabel.place(relx=0.2, rely=0.4)

        self.requestedTempLabel = tk.Label(self, text=self.requestedtTempString, font=controller.temp_font)
        self.requestedTempLabel.place(relx=0.2, rely=0.5)


        ################################
        #                              #
        #     TEMPERTURE_BUTTONS       #
        #           SETTINGS           #
        #                              #
        ################################

        # Up and Down Arrows Images
        upArrow = tk.PhotoImage(file = "up_arrow.gif")
        downArrow = tk.PhotoImage(file = "down_arrow.gif")

        self.upButton = tk.Button(self, image = upArrow, command= self.tempUp)
        self.upButton.image = upArrow
        self.upButton.place(relx=0.2, rely =0.6)
        self.downButton = tk.Button(self, image = downArrow, command= self.tempDown)
        self.downButton.place(relx=0.4, rely=0.6)
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
        #
        # label = tk.Label(self, text="This is cities page!", font=controller.temp_font)
        # label.grid(row = 0, column = 0)

        variable = tk.StringVar(self)
        variable.set("City") # default value


        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(padx = 10)


        cityOptions = tk.OptionMenu(self, variable, "Los Angeles,CA", "Las Vegas,NV", "New York,NY","Miami,FL","SEOUL, South Korea","São Paulo, Brazil"
        "Bombay, India", "JAKARTA, Indonesia","Karachi, Pakistan","MOSKVA (Moscow), Russia","Istanbul, Turkey")
        cityOptions.pack(fill='x')

class CalendarPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
            
        button.pack(padx = 10)
        def print_sel():
            print(cal.selection_get())
        
        cal = Calendar(self,font="Arial 14", selectmode='day',cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        tk.Button(self, text="ok", command=print_sel).pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
