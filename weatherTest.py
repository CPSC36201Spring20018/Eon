from weather import Weather, Unit

def threeDayForecast(loc):
    weather = Weather(unit=Unit.FAHRENHEIT)
    location = weather.lookup_by_location(loc)
    condition = location.condition
    forecasts = location.forecast
    for i in range(3):
        print(forecasts[i].day)
        print(forecasts[i].date)
        print(forecasts[i].high)
        print()

def locationTemperature(loc):
    weather = Weather(unit=Unit.FAHRENHEIT)
    location = weather.lookup_by_location(loc)
    condition = location.condition
    temperature = condition.temp
    print(temperature)

loca = 'Long Beach,CA'
threeDayForecast(loca)
loca = 'New York,NY'
locationTemperature(loca)

