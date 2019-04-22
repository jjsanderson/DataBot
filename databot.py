"""DataBot - display atmospheric pressure on a Pimoroni ScrollBot.
"""

import pyowm
from pypollen import Pollen
from clientsecrets import owmkey

owm = pyowm.OWM(owmkey)

latitude = 55.03973
longitude = -1.44713

# OpenWeatherMap current report
# observation = owm.weather_at_place('Whitley Bay,GB')
observation = owm.weather_at_id(2634032) # Prefer this approach if possible
w = observation.get_weather()
print(w)

pressure = w.get_pressure()['press']
print(pressure)

# Benadryl Pollen Forecast data
print(Pollen(latitude, longitude).pollencount)