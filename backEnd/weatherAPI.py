import ipLocation
from weather import Weather, Unit

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

loca = ipLocation.location()
loca = loca[0] + ',' + loca[1]
print(loca)
print("it is currently ", locationTemperature(loca), " in ", loca)
print()
forecast = threeDayForecast(loca)
for i in range(1,4):
    print(forecast[i].day)
    print(forecast[i].high)
    print(forecast[i].text)
    print()
loca = 'New York,NY'
print("it is currently ", locationTemperature(loca), " in ", loca)

