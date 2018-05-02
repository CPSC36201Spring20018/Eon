import backEnd.calendarAPI as calendarAPI
import backEnd.HVAC_Controller as HVAC_Controller
import backEnd.ipLocation as ipLocation
import backEnd.weatherAPI as weatherAPI
#import backEnd.tempRead as tempRead
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
        r_temp = 0
        event_list = None
        personal_location = None

    def getLocation(self):
        city, state = ipLocation.location()
        return str(city)+','+str(state)

    def getForecast(self, location):
        return weatherAPI.threeDayForecast(location)

    def getCityTemp(self, location):
        return weatherAPI.locationTemperature(location)

    def getTemperature(self):
        return tempRead.read_temp()

    def getCalendar(self):
        return calendarAPI.list()

    def deleteCalendarEvent(self, eventID):
        calendarAPI.delete(eventID)

    def createCalendarEvent(self, summary, start, end, day):
        calendarAPI.create(summary, start, end, day)

    def setTemperature(self, temp):
        self.r_temp = temp

    def activateAC(self):
        HVAC_Controller.ACOn()

    def deactivateAC(self):
        HVAC_Controller.ACOff()

    def activateHeat(self):
        HVAC_Controller.HeatOn()

    def deactivateHeat(self):
        HVAC_Controller.HeatOff()

if __name__ == "__main__":
    main()
