import re
import json
from urllib.request import urlopen

def location():
    url = 'http://ipinfo.io/json'
    response =urlopen(url)
    data = json.load(response)

    city = data['city']
    region = data['region']
    return(city,region)

print(location())
