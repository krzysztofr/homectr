import ephem
from datetime import timedelta
from settings import devices_definitions
from models import Device

waw = ephem.city('Warsaw')
prev_setting = round((timedelta(waw.date - waw.previous_setting(ephem.Sun())).seconds/60),0)
next_sunrise = round((timedelta(waw.previous_setting(ephem.Sun()) - waw.date).seconds/60),0)

print "previous settings was: " + str(prev_setting) + " minutes ago"
print "next sunrise will be in: " + str(next_sunrise) + " minutes"

devices = {}

for d in devices_definitions:
    devices[d['pin']] = Device(name=d['name'], pin=d['pin'], action=d['action'], reset_state=False)

# jezeli prev_setting < 15 && stan == 0 -> zmienic na 1
# jezeli next_sunrise < 15 && stan == 1 -> zmienic na 0


if prev_setting < 15 and devices[15].read_state() == 0:
    devices[15].switch()
if next_sunrise < 15 and devices[15].read_state() == 1:
    devices[15].switch()




