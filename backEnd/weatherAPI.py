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
