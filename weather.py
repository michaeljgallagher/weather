#!/usr/bin/env python3

import requests
from datetime import datetime


def get_location():
    r = requests.get('https://ipinfo.io/json')
    data = r.json()
    loc, city, region, country = data['loc'].split(','),\
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
    if deg >= 11.25 and deg < 33.75:
        return 'NNE'
    elif deg >= 33.75 and deg < 56.25:
        return 'NE'
    elif deg >= 56.25 and deg < 78.75:
        return 'ENE'
    elif deg >= 78.75 and deg < 101.25:
        return 'E'
    elif deg >= 101.25 and deg < 123.75:
        return 'ESE'
    elif deg >= 123.75 and deg < 146.25:
        return 'SE'
    elif deg >= 146.25 and deg < 168.75:
        return 'SSE'
    elif deg >= 168.75 and deg < 191.25:
        return 'S'
    elif deg >= 191.25 and deg < 213.75:
        return 'SSW'
    elif deg >= 213.75 and deg < 236.25:
        return 'SW'
    elif deg >= 236.25 and deg < 258.75:
        return 'WSW'
    elif deg >= 258.75 and deg < 281.25:
        return 'W'
    elif deg >= 281.25 and deg < 303.75:
        return 'WNW'
    elif deg >= 303.75 and deg < 326.25:
        return 'NW'
    elif deg >= 326.25 and deg < 348.75:
        return 'NNW'
    else:
        return 'N'


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
        wdeg = ''
        wdirec = ''
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
