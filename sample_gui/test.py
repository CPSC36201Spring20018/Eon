##############################################
# Created on: 
# Written by: 
#
##############################################
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
        for F in (StartPage, SettingsPage, CityPage, CalendarPage):
            page_name = F.__name__
            
            frame = F(parent = container, controller=self)
            
            #spaceImage = tk.PhotoImage(file = "space.gif")
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

    def tempUp(self):
        if(self.requestedTemperature > 60):
            self.requestedTemperature -= 1
            self.requestedtTempString = str(self.requestedTemperature)+"°F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.downButton.config(state="normal")
        else:
            self.upButton.config(state="disable")

    def tempDown(self):
        if(self.requestedTemperature < 90):
            self.requestedTemperature += 1
            self.requestedtTempString = str(self.requestedTemperature)+"°F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.upButton.config(state="normal")
        else:
            self.downButton.config(state="disable")

    def systemToggle(self):
        if(self.isOn == True):
            self.isOn = False
            powerImage = tk.PhotoImage(file = "powerOff.png")
            self.systemOnOffButton.configure(image = powerImage)
            self.systemOnOffButton.photo = powerImage
            self.systemOnOffButton.configure(text = "Off")
        else:
            self.isOn = True
            powerImage = tk.PhotoImage(file = "powerOn.png")
            self.systemOnOffButton.configure(image = powerImage)
            self.systemOnOffButton.photo = powerImage
            self.systemOnOffButton.configure(text = "On")

    def vacayToggle(self):
        if(self.vacayIsOn == True):
            self.vacayIsOn = False
            vacayImage = tk.PhotoImage(file ="airplaneModeOff.png")
            self.vacayButton.configure(image = vacayImage)
            self.vacayButton.photo = vacayImage
            self.systemOnOffButton.configure(text = "Off")

        else:
            self.vacayIsOn = True
            self.systemOnOffButton.configure(text = "On")
            vacayImage = tk.PhotoImage(file ="airplaneModeOn.png")
            self.vacayButton.configure(image = vacayImage)
            self.vacayButton.photo = vacayImage



    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.vacayIsOn = False
        self.isOn = True
        self.currentTemperature = 80
        self.requestedTemperature = 70
        backgroundImage = tk.PhotoImage(file = "bg.png")
        background = tk.Label(self, image = backgroundImage)
        background.place(x=0, y=0, relwidth=1, relheight=1)
        background.image = backgroundImage
        ################################
        #                              #
        #       TIME_WIFI_SYSTEM       #
        #           SETTINGS           #
        ################################

       	wifiImage = tk.PhotoImage(file = "wifi.png")
	
        wifiLabel = tk.Label(self, image = wifiImage, bg = 'black')
        wifiLabel.place(relx=0.95, rely = 0.01)
        wifiLabel.image = wifiImage
        
	# Current Time being display top right corner
        now = datetime.datetime.now().time()

        timeLabel = tk.Label(self, text=now.strftime("%I:%M %p"), font=controller.time_font, bg = 'black', fg = 'white')
        timeLabel.config(font = ("Calibri", 17))
        timeLabel.place(relx = 0.55,rely = 0.35)
       
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
        powerButton = tk.PhotoImage(file = "powerOn.png")
        self.systemOnOffButton = tk.Button(self, image = powerButton, relief = 'flat', command= self.systemToggle, bg = 'black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        self.systemOnOffButton.image = powerButton
        self.systemOnOffButton.place(relx=.05, rely = 0.01)
        
	# settings button
        settingsImage = tk.PhotoImage(file = "settings.png")
        settingsButton = tk.Button(self, image = settingsImage, relief= 'flat',command=lambda: controller.show_frame("SettingsPage"), bg ='black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        settingsButton.image = settingsImage
        settingsButton.place(relx=0.1, rely=0.01)

	# vacation button
        vacayImage = tk.PhotoImage(file = "airplaneModeOff.png")
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
            forecast = threeDayForecast(value)
            self.requestedTemperature = forecast[0].high
            self.requestedTempLabel.configure(text = str(self.requestedTemperature) +"°F")
            self.requestedTemperature = int(self.requestedTemperature)
    
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
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        city = j['city']
        reg_code = j['region_code']
        locat = city + ',' + reg_code
        self.variable.set(locat)
        
        # Uses weather API to get three day forecast
        # Will forecast next three days, not today's forecast
        days = [None] * 4
        temp = [None] * 4
        forecast = threeDayForecast(self.variable.get())

        for i in range(0,4):
            days[i] = forecast[i].day
            temp[i] = forecast[i].high + "°F"
            print(locat)
        weatherImageArray = [None] * 4
        for i in range(0,4):
            weatherImageSearch = forecast[i].text
            if weatherImageSearch == "Sunny":
                weatherImage = tk.PhotoImage(file = "sunny.png")
            if weatherImageSearch == "Partly Cloudy":
                weatherImage = tk.PhotoImage(file = "partlyCloudy.png")
            if weatherImageSearch == "Mostly Cloudy":
                weatherImage = tk.PhotoImage(file = "mostlyCloudy.png")
            if weatherImageSearch == "Cloudy":
                weatherImage = tk.PhotoImage(file = "cloudy.png")
           
            weatherLabel = tk.Label(self, image =  weatherImage, bg = 'black')
            weatherLabel.image =  weatherImage
            weatherImageArray[i] = weatherLabel

        day1String = tk.StringVar()
        day1String.set(days[1])
        day1TempString = tk.StringVar()
        day1TempString.set(temp[1])

        day2String = tk.StringVar()
        day2String.set(days[2])
        day2TempString = tk.StringVar()
        day2TempString.set(temp[2])

        day3String = tk.StringVar()
        day3String.set(days[3])
        day3TempString = tk.StringVar()
        day3TempString.set(temp[3])

        # Label for the three day forecast
        day1Label = tk.Label(self, text=day1String.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day1TempLabel = tk.Label(self, text=day1TempString.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day1TempLabel.place(relx=0.85, rely=0.65)
        day1Label.place(relx=0.55, rely=0.65)
        weatherImageArray[1].place(relx=0.725, rely=0.65)

        day2Label = tk.Label(self, text=day2String.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day2TempLabel = tk.Label(self, text=day2TempString.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day2TempLabel.place(relx =0.85, rely = 0.75)
        day2Label.place(relx=0.55, rely=0.75)
        weatherImageArray[2].place(relx=0.725, rely=0.75)

        day3Label = tk.Label(self, text=day3String.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day3TempLabel = tk.Label(self, text=day3TempString.get(), font=controller.day_font, bg = 'black',fg = 'white')
        day3TempLabel.place(relx=0.85, rely=0.85)
        day3Label.place(relx=0.55, rely=0.85)
        weatherImageArray[3].place(relx=0.725, rely=0.85)


        ################################
        #                              #
        #         TEMPERATURE          #
        #           SETTINGS           #
        #                              #
        ################################


	# outdoor temperature

        outdoorTextLabel = tk.Label(self, text = self.variable.get(),font = ("Calibri, 15"),bg = 'black',fg = 'white')
        outdoorTextLabel.place(relx=0.55, rely=0.5)
        self.currentTemperature = temp[0]
        self.currentTempString = str(self.currentTemperature)
        self.currentTempLabel = tk.Label(self, text=self.currentTempString, font=controller.temp_font, bg = 'black',fg = 'white')
        self.currentTempLabel.config(font = ("Calibri", 17))
        self.currentTempLabel.place(relx=0.85, rely=0.5)

	# indoor temperature
        self.requestedtTempString = str(self.requestedTemperature)+"°F"
        self.requestedTempLabel = tk.Label(self, text=self.requestedtTempString, font=controller.temp_font, bg = 'black',fg = 'white')
        self.requestedTempLabel.place(relx=0.2, rely=0.3)


        ################################
        #                              #
        #     TEMPERTURE_BUTTONS       #
        #           SETTINGS           #
        #                              #
        ################################

        # Up and Down Arrows Images
        upArrow = tk.PhotoImage(file = "up.png")
        downArrow = tk.PhotoImage(file = "down.png")

        self.upButton = tk.Button(self, image = upArrow, relief = 'flat',command= self.tempUp, bg = 'black', highlightbackground = 'black', highlightcolor = 'black',activebackground='#333333', activeforeground = 'white')
        self.upButton.image = upArrow
        self.upButton.place(relx=0.09, rely =0.55)
        self.downButton = tk.Button(self, image = downArrow, relief = 'flat', command= self.tempDown, bg = 'black', highlightbackground = 'black',activebackground='#333333', activeforeground = 'white')
        self.downButton.place(relx=0.35, rely=0.55)
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
        now = datetime.datetime.now()
        cal = Calendar(self,font="Arial 14", selectmode='day',cursor="hand1", year=now.year, month=now.month, day=now.day)
        cal.pack(fill="both", expand=True)
        tk.Button(self, text="ok", command=print_sel).pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
