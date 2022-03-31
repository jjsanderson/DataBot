"""DataBot 2.0 - display weather and related data on Pimoroni ScrollpHAT
"""

import pyowm
import time
from threading import Timer
from pyquery import PyQuery as pq
from clientsecrets import owmkey

# You'll need an Open Weather Map API key, stored in a clientsecrets.py file:
# owmkey = 'your_key_here'
# OWM query object here as a global, because I'm lazy.
owm = pyowm.OWM(owmkey)
mgr = owm.weather_manager()

# Lat and long for where I live; replace as you wish.
latitude = 55.03973
longitude = -1.44713


class RepeatedTimer(object):
    """Simple timer class, from StackExchange (obviously).

    Credit: user MestreLion, https://stackoverflow.com/questions/3393612

    Modified to allow change of interval without tearing down the timer.
    """

    def __init__(self, interval, function, *args):
        """Initialize the timer object."""
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.is_running = False
        self.start()

    def _run(self):
        """Timer has been triggered: execute callback function."""
        self.is_running = False
        self.start()
        self.function(*self.args)

    def start(self):
        """Start the timer, if it's not already running."""
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        """Stop the timer."""
        self._timer.cancel()
        self.is_running = False

    def bpm(self, newBPM):
        """Reset the interval to new beats per minute."""
        self.interval = (60/newBPM)


class DataBot(object):
    """DataBot 2.0 - display weather and related data on Pimoroni ScrollpHAT

    This is a simple weather display for the Pimoroni Scroll pHAT HD.
    It uses the Open Weather Map API to get the current weather.
    """

    def __init__(self, interval, showTime):
        """Initialize the weather display object."""
        self.interval = interval
        self.showTime = showTime
        self.timer = RepeatedTimer(self.interval, self.update)
        self.timer.start()

    def update(self):
        """Update the weather display."""
        # Get the weather data
        observation = mgr.weather_at_coords(latitude, longitude)
        weather = observation.weather
        # Get the current temperature
        temp = weather.temperature('celsius')['temp']
        # Get the current pressure
        pressure = weather.pressure()['press']
        # Get the current humidity
        humidity = weather.humidity
        # Get the current pollen level
        pollen = self.getPollen()
        # Display the weather data
        self.display(temp, pressure, humidity, pollen)

    def display(self, temp, pressure, humidity, pollen):
        """Display the weather data on the Scroll pHAT HD."""
        # Clear the display
        scrollphathd.clear()
        # Set the brightness
        scrollphathd.set_brightness(BRIGHTNESS)
        # Display the temperature
        scrollphathd.write_string('{:.1f}'.format(temp), x=0, y=0, font=font5x7, brightness=1.0)
        # Display the pressure
        scrollphathd.write_string('{:.0f}'.format(pressure), x=0, y=8, font=font5x7, brightness=1.0)
        # Display the humidity
        scrollphathd.write_string('{:.0f}'.format(humidity), x=0, y=16, font=font5x7, brightness=1.0)
        # Display the pollen level
        scrollphathd.
