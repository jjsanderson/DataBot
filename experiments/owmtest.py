import pyowm
from clientsecrets import owmkey

owm = pyowm.OWM(owmkey)
mgr = owm.weather_manager()

observation = mgr.weather_at_id(2634032)
print(observation.weather)
print(observation.weather.temperature('celsius')["temp"])
print(observation.weather.humidity)
print(observation.weather.pressure["press"])
