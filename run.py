#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

import time
import RPi.GPIO as GPIO
from pyowm import OWM

owm = OWM('45986823d1c4a9d000d4b14821710a8e')

reg = owm.city_id_registry()# lots of results
list_of_tuples = SH = reg.ids_for('Birmingham', country='GB') # only one: [ (1796236,, 'Birmingham, GB  ') ]
# Search for current weather in Birmingham, UK
mgr = owm.weather_manager()
observation = mgr.weather_at_place('Birmingham,GB')
w = observation.weather # <Weather - reference_time=2020-07-06 12:06:51+00,
print(w) #status=rain, detailed_status=light intensity shower rain>
# Weather details
w_2 = w.wind()                  # {'speed': 4, 'deg': 300}
w_3 = w.humidity                # 100
w_4 = w.temperature('celsius')  # {'temp': 23.4, 'temp_max': 23.89, 'temp_min': 22.78, #'feels_like': 26.07, 'temp_kf': None} #w_4 = int
status = w.detailed_status
speed = w.wind().get('speed',0)
temp = w.temperature('celsius').get('temp',0)

print("The wind speed is", w_2)
print("The humidity is", w_3)
print("The temperature is", w_4)

print("Status:", status)
print("Windspeed:",speed)
print("Temperature:",temp)

lcd = LCD()

def safe_exit(signum, frame):
    exit(1)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    status = w.detailed_status
    speed = "Windspeed: " + str(float(w.wind().get('speed', 0)))
    temp = "Temperature: " + str(float(w.temperature('celsius').get('temp', 0)))

    lcd.text("Status:".center(20), 1)
    lcd.text(status.center(20), 2)
    lcd.text(speed.center(20), 3)
    lcd.text(temp.center(20), 4)
    
    pause()
except KeyboardInterrrupt:
    pass

finally:
    lcd.clear()