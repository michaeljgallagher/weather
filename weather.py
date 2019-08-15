import requests
import json

def get_location():
    ipinfo = requests.get('https://ipinfo.io/json')
    data = json.loads(ipinfo.text)
    loc, city, region, country = data['loc'], data['city'], data['region'], data['country']
    return loc, city, region, country

def get_weather(loc):
    url = 'https://api.weather.gov/points/' + loc
    req = requests.get(url)
    data = json.loads(req.text)    
    url2 = data['properties']['forecast']
    req2 = requests.get(url2)
    data2 = json.loads(req2.text)
    return data2['properties']['periods'][0]

def display_weather(data):
    print("""
    Temperature : {temp} F
    Wind : {wspeed} {wdirec}
    Forecast : {detfor}
    """.format(temp = data['temperature'], wspeed = data['windSpeed'], wdirec = data['windDirection'], detfor = data['detailedForecast'])
          )

def main():
    loc, city, region, country = get_location()
    print('Weather for {}, {}, {} :'.format(city, region, country))
    data = get_weather(loc)
    display_weather(data)

if __name__ == '__main__':
    main()
