import argparse
import requests
from datetime import datetime

URL = 'https://api.openweathermap.org/data/2.5/weather'
KEY = 'f4f5a4d6512d7a503f2085717a52eaf9'


def get_location():
    r = requests.get('https://ipinfo.io/json')
    data = r.json()
    loc, city, region, country = data['loc'].split(','), data['city'], data['region'], data['country']
    return loc, city, region, country


def get_weather_by_loc(loc):
    params = {'appid': KEY,
              'lat': loc[0],
              'lon': loc[1],
              'units': 'imperial'
              }
    r = requests.get(URL, params=params)
    data = r.json()
    return data


def get_weather_by_zip(zipcode, country='us'):
    params = {'appid': KEY,
              'zip': f'{zipcode},{country}',
              'units': 'imperial'
              }
    r = requests.get(URL, params=params)
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
    print(f"""
    Currently : {temp} F, {cond}
    Min Temp: {mintemp} F, Max Temp: {maxtemp} F
    Wind : {wspeed} MPH {wdirec} ({wdeg} degrees)
    Humidity : {humidity}%
    Forecast : {fc}
    Sunrise : {sunrise}, Sunset : {sunset}
    """)


def main():
    parser = argparse.ArgumentParser(description='Display the current weather')
    parser.add_argument('-z', '--zip', action='store', nargs='+', help='specify a postal code and/or a country code')
    args = parser.parse_args()
    if args.zip:
        data = get_weather_by_zip(*vars(args)['zip'])
        if data['cod'] == '404':
            print('Invalid postal code / city not found')
        else:
            city, country = data['name'], data['sys']['country']
            print(f'\nWeather for {city}, {country} :')
            display_weather(data)
    else:
        loc, city, region, country = get_location()
        data = get_weather_by_loc(loc)
        print(f'\nWeather for {city}, {region}, {country} :')
        display_weather(data)


if __name__ == '__main__':
    main()
