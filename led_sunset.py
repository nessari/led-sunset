#!/usr/bin/python3

import os

from astral import today, LocationInfo
from astral.sun import sun

city = LocationInfo(name='Budapest', region='Hungary', timezone='Europe/Budapest', latitude=47.4979937, longitude=19.0403594)
sunset = sun(city.observer, today(), tzinfo=city.tzinfo)['sunset'].strftime('%H:%M')

os.system(f"echo '/usr/sbin/uhubctl -l 1-1 --ports 2 -a 1' | at {sunset}")
