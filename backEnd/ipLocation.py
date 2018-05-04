import requests
import json

def location():
    # region_code url http://freegeoip.net/json
    # sean's orginal json request site http://ipinfo.io/json
    url = 'http://freegeoip.net/json'
    response =requests.get(url)
    data = json.loads(response.text)

    city = data['city']
    region = data['region_code']
    return(city,region)
