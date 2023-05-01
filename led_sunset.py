#!/usr/bin/python3

from datetime import datetime, timedelta

import json
import os
import subprocess
import sys

import requests

LATITUDE = '47.4979937'
LONGITUDE = '19.0403594'

CACHE_NAME = 'sunsets.json'

COMMAND = 'uhubctl -l 1-1 --ports 2 -a 1'.split()

five_minutes = timedelta(minutes=5)
now = datetime.now()
today = datetime.today()

# TODO: calculate time zone and dst shifts
# adjust for timezone and summer shifts (CEST, DST)

def parse_time(time_string):
    format = '%I:%M:%S %p'
    time = datetime.strptime(time_string, format)
    sunset_time = datetime.combine(today.date(), time.time())
    return sunset_time

def shift_time(time_string, offset):
    """Shifts the string representation of time by the specified number of hours"""
    shifted = parse_time(time_string) + timedelta(hours=offset)
    return shifted.strftime('%I:%M:%S %p')

def get_data_from_API():
    sunsets = []
    # create dates for the upcoming week
    week = [(today + timedelta(days=x)).strftime('%Y-%m-%d') for x in range (7)]
    # call sunrise-sunset API
    for date in week:
        URL = f'https://api.sunrise-sunset.org/json?lat={LATITUDE}&lng={LONGITUDE}&date={date}'
        resp = json.loads(requests.get(URL).text)
        sunset = shift_time(resp['results']['sunset'], 2)
        sunsets.append(sunset)
    weekly_sunsets = dict(zip(week, sunsets))
    return weekly_sunsets

def cache():
    sunsets = get_data_from_API()
    # write data to json file
    with open(CACHE_NAME, 'w') as file:
        json.dump(sunsets, file)

def switch_if_sun_sets():
    # check if there is cached data, otherwise bail out
    if not os.path.exists(CACHE_NAME):
        sys.exit('No cached data! Run with the --cache flag first!')

    # read todays sunset from json
    with open(CACHE_NAME) as sunset_data:
        cached_sunsets = json.load(sunset_data)

    todays_sunset = parse_time(cached_sunsets[str(today.date())])

    # switch usb on
    if now >= (todays_sunset - five_minutes) and now < (todays_sunset + five_minutes):
        subprocess.run(COMMAND)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        switch_if_sun_sets()
    elif len(sys.argv) == 2 and sys.argv[1] == '--cache':
        cache()
