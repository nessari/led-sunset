import datetime
import json

import requests

# create dates for the upcoming week

today = datetime.datetime.today()
print(today)

week = [(today + datetime.timedelta(days=x)).strftime('%Y-%m-%d') for x in range (7)]
print(week)

# TODO: calculate time zone and dst shifts
# CEST, DST


# call sunrise-sunset API

latitude = '47.4979937'
longitude = '19.0403594'

sunsets = []

for date in week:
    URL = f'https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={date}'
    resp = json.loads(requests.request('GET', URL).text)
    sunset = resp['results']['sunset']
    sunsets.append(sunset)

print(sunsets)

weekly_sunsets = dict(zip(week, sunsets))
print(weekly_sunsets)

# write data to json file

with open('sunsets.json', 'w') as file:
    json.dump(weekly_sunsets, file)


# TODO: adjust for time zone and summer shifts