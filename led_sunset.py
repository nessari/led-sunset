from datetime import datetime, time, timedelta
import json
import subprocess

import requests

latitude = '47.4979937'
longitude = '19.0403594'

switch_off_time = time(21, 30)
print('Switch off time: ', switch_off_time)

five_minutes = timedelta(minutes=5)

now = datetime.now()
print('Now: ', now)
print('Current time: ', now.time())

# create dates for the upcoming week

today = datetime.today()
# print(today)
# print(today.date())

week = [(today + timedelta(days=x)).strftime('%Y-%m-%d') for x in range (7)]
print('Dates of the week:', week)

# TODO: calculate time zone and dst shifts
# CEST, DST

sunsets = []

def format_time(time_string):
    format = '%I:%M:%S %p'
    time = datetime.strptime(time_string, format)
    return time

# call sunrise-sunset API

for date in week:
    URL = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date}'
    resp = json.loads(requests.request('GET', URL).text)
    sunset = resp['results']['sunset']
    sunsets.append(sunset)

print('Sunsets', sunsets)

weekly_sunsets = dict(zip(week, sunsets))
print('Data to json: ', weekly_sunsets)

# write data to json file

with open('sunsets.json', 'w') as file:
    json.dump(weekly_sunsets, file)


# TODO: adjust for time zone and summer shifts

# read todays sunset from json

with open('sunsets.json') as sunset_data:
    cached_sunsets = json.load(sunset_data)
print('Cached sunsets', cached_sunsets)

todays_sunset = cached_sunsets[str(today.date())]
print('Todays sunset: ', todays_sunset)

formatted = format_time(todays_sunset)
print('Sunset formatted: ', formatted)

cest_sunset = formatted + timedelta(hours=2)
print('CEST sunset: ', cest_sunset)

# switch ubs off and on

if now >= (formatted - five_minutes) and now <= (formatted + five_minutes):
    print('Switch on!')
else:
    print('Switch off!')
