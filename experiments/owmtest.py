import pyowm
from clientsecrets import owmkey

owm = pyowm.OWM(owmkey)
mgr = owm.weather_manager()

observation = mgr.weather_at_id(2634032)
print(observation.weather)
print(observation.weather.temperature('celsius')["temp"])
print(observation.weather.humidity)
print(observation.weather.pressure["press"])

tempReport = observation.weather.temperature('celsius')['temp']
print(tempReport)
print(round(tempReport, 1))
# round the tempReport to 1 dp, cast to string, append 'C'
print( str(round(tempReport, 1)) + "C" )
