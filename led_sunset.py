#!/usr/bin/python3

from datetime import datetime, timedelta

import json
import subprocess
import sys

import requests

LATITUDE = '47.4979937'
LONGITUDE = '19.0403594'

five_minutes = timedelta(minutes=5)
now = datetime.now()
today = datetime.today()

# TODO: calculate time zone and dst shifts
# adjust for timezone and summer shifts (CEST, DST)

def parse_time(time_string):
    format = '%I:%M:%S %p'
    time = datetime.strptime(time_string, format)
    return time

def get_data_from_API():
    sunsets = []
    # create dates for the upcoming week
    week = [(today + timedelta(days=x)).strftime('%Y-%m-%d') for x in range (7)]
    # call sunrise-sunset API
    for date in week:
        URL = f'https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}&date={date}'
        resp = json.loads(requests.get(URL).text)
        sunset = resp['results']['sunset']
        sunsets.append(sunset)
    weekly_sunsets = dict(zip(week, sunsets))
    return weekly_sunsets

def cache():
    sunsets = get_data_from_API()
    print('Sunsets', sunsets)
    # write data to json file
    with open('sunsets.json', 'w') as file:
        json.dump(sunsets, file)

def switch_if_sun_sets():
    # read todays sunset from json
    with open('sunsets.json') as sunset_data:
        cached_sunsets = json.load(sunset_data)

    todays_sunset = parse_time(cached_sunsets[str(today.date())])
    cest_sunset = todays_sunset + timedelta(hours=2)

    # switch usb on
    if now >= (cest_sunset - five_minutes) and now <= (cest_sunset + five_minutes):
        subprocess.run(['uhubctl', '-l', '1-1', '--ports', '2', '-a', '1'])

if __name__ == '__main__':
    if len(sys.argv) == 1:
        switch_if_sun_sets()
    elif len(sys.argv) == 2 and sys.argv[1] == '--cache':
        cache()