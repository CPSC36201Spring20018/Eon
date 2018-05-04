# import backEnd.calendarAPI as calendarAPI   # Needed for googleapis
# import backEnd.HVAC_Controller as HVAC_Controller  # Needed for GPIO
import backEnd.ipLocation as ipLocation
import backEnd.weatherAPI as weatherAPI
# import backEnd.tempRead as tempRead # Needed for GPIO
import datetime as dt


def main():
    x = Controller()
    cityLocation = 'Moscow, RU'
    x.setTemperature(90)
    print('user input temperature: {}'.format(x.r_temp))
    x.personalLocation = x.getLocation()
    print(x.personalLocation)
    forecast = x.getForecast(x.personalLocation)
    for i in range(1,4):
        print(forecast[i].text)
        print(forecast[i].date)
        print(forecast[i].high)
    x.setTemperature(x.getCityTemp(cityLocation))
    print('city was {0}, temperature set to: {1}'.format(cityLocation,x.r_temp))
    x.createCalendarEvent('60',(dt.datetime.now()+dt.timedelta(minutes=1)).isoformat(),(dt.datetime.now()+dt.timedelta(minutes=60)).isoformat(),'WE')
    calendar = x.getCalendar()
    #print(calendar)
    x.setTemperature(int(calendar['items'][0]['summary']))
    print('calendar input from event = {0} input temperature: {1}'.format(calendar['items'][0]['id'],x.r_temp))
    print('\neventId\t\t\t\t\tstart date and time\ttemperature\n')
    for event in calendar['items']:
        print(event['id'],'\t',event['start']['dateTime'],'\t',event['summary'])
    #x.deleteCalendarEvent(calendar['items'][0]['id'])
    #calendar = x.getCalendar()
    #for event in calendar['items']:
    #    print(event['id'],event['start']['dateTime'],event['summary'])

class Controller():

    def __init__(self):
        self.requested_temperature = 0
        self.current_temperature = 0
        self.threshold = 3
        self.isH = False
        self.isA = False
        self.isDisable = False
        self.isVacation = False

    def getLocation(self):
        city, state = ipLocation.location()
        return str(city)+','+str(state)

    def getForecast(self, location):
        return weatherAPI.threeDayForecast(location)

    def getCityTemperature(self, location):
        return weatherAPI.locationTemperature(location)

    def setCurrentTemperature(self):
        self.current_temperature = int(tempRead.read_temp()[1])

    def getCurrentTemperature(self):
        return self.current_temperature

    def setRequestedTemperature(self, temp):
        self.requested_temperature = temp

    def getRequestedTemperature(self):
        return self.requested_temperature

    def getCalendar(self):
        return calendarAPI.list()

    def deleteCalendarEvent(self, eventID):
        calendarAPI.delete(eventID)

    def createCalendarEvent(self, summary, start, end, day):
        calendarAPI.create(summary, start, end, day)

    def activateAC(self):
        if not self.isDisable:
            self.isA = HVAC_Controller.ACOn()
        else:
            print("System Disabled")

    def deactivateAC(self):
        self.isA = HVAC_Controller.ACOff()

    def activateHeat(self):
        if not self.isDisable or self.isVacation:
            self.isH = HVAC_Controller.HeatOn()
        else:
            print("System Disabled")

    def deactivateHeat(self):
        self.isH = HVAC_Controller.HeatOff()

    def isAC(self):
        return self.isA

    def isHeat(self):
        return self.isH

    def Disable(self):
        if self.isAC():
            self.deactivateAC()
        if self.isHeat():
            self.deactivateHeat()
        self.isDisable = True

    def Enable(self):
        self.isDisable = False

    def setVacation(self):
        if not self.isVacation:
            self.setRequestedTemperature(40)
            self.isVacation = True
            self.Disable()
        else:
            self.isVacation = False
            self.Enable()

#if __name__ == "__main__":
#    main()
