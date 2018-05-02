import requests
import json

def location():
    url = 'http://ipinfo.io/json'
    response =requests.get(url)
    data = json.loads(response.text)

    city = data['city']
    region = data['region']
    return(city,region)

#print(location())
