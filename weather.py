#!/usr/bin/env python3

import requests
from datetime import datetime


def get_location():
    r = requests.get('https://ipinfo.io/json')
    data = r.json()
    loc, city, region, country = data['loc'].split(','), \
                                 data['city'], data['region'], data['country']
    return loc, city, region, country


def get_weather(loc):
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'APPID': 'f4f5a4d6512d7a503f2085717a52eaf9',
              'lat': loc[0],
              'lon': loc[1],
              'units': 'imperial'}
    r = requests.get(url, params=params)
    data = r.json()
    return data


def degrees_to_cardinal(deg):
    dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
    i = int((11.25 + deg) / 22.5)
    return dirs[i % 16]


def display_weather(data):
    temp = data['main']['temp']
    cond = data['weather'][0]['main']
    mintemp = data['main']['temp_min']
    maxtemp = data['main']['temp_max']
    wspeed = data['wind']['speed']
    if 'deg' in data['wind'].keys():
        wdeg = data['wind']['deg']
        wdirec = degrees_to_cardinal(wdeg)
    else:
        wdeg = None
        wdirec = None
    humidity = data['main']['humidity']
    fc = data['weather'][0]['description'].capitalize()
    tz = data['timezone']
    sr = data['sys']['sunrise'] + tz
    ss = data['sys']['sunset'] + tz
    sunrise = datetime.utcfromtimestamp(sr).strftime('%H:%M')
    sunset = datetime.utcfromtimestamp(ss).strftime('%H:%M')
    print("""
    Currently : {} F, {}
    Min Temp: {} F, Max Temp: {} F
    Wind : {} MPH {} ({} degrees)
    Humidity : {}%
    Forecast : {}
    Sunrise : {}, Sunset : {}
    """.format(temp, cond, mintemp, maxtemp, wspeed, wdirec, wdeg, humidity,
               fc, sunrise, sunset)
          )


def main():
    loc, city, region, country = get_location()
    print('Weather for {}, {}, {} :'.format(city, region, country))
    data = get_weather(loc)
    display_weather(data)


if __name__ == '__main__':
    main()
