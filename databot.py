"""DataBot - display atmospheric pressure on a Pimoroni ScrollBot.
"""

import pyowm
import time
from threading import Timer
from pypollen import Pollen
from clientsecrets import owmkey

owm = pyowm.OWM(owmkey)

latitude = 55.03973
longitude = -1.44713

interval = 10 # seconds between API data updates

pressureReport = 0
pollenReport = "NAN"

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


def updatePressure():
    """Fetch pressure data from OpenWeatherMap.
    
    Triggered on a timer to avoid overloading API.
    """
    global pressureReport
    # observation = owm.weather_at_place('Whitley Bay,GB')
    observation = owm.weather_at_id(2634032) # Prefer this approach if possible
    w = observation.get_weather()
    pressureReport = w.get_pressure()['press']
    return pressureReport


def updatePollen():
    """Fetch pollen data from Benadryle / Met. Office.

    Triggered on a timer to avoid overloading API.
    """
    global pollenReport
    pollenReport = Pollen(latitude, longitude).pollencount
    return pollenReport


def displayClock():
    """Documentation string.
    """

    timeString = time.strftime("%H:%M")
    print(timeString)
    time.sleep(1)


if __name__ == "__main__":
    
    # Get data on initial start
    pressureReport = updatePressure()
    pollenReport = updatePollen()

    # Start the data update timers
    rtPressure = RepeatedTimer(interval, updatePressure)
    rtPollen = RepeatedTimer(interval, updatePollen)

    # ...and now we can loop
    while True:
        displayClock()
        displayClock()
        print(pressureReport)
        time.sleep(2)
        print(pollenReport)
        time.sleep(2)
