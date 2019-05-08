"""DataBot - display atmospheric pressure on a Pimoroni ScrollBot.
"""

import pyowm
import time
import scrollphathd
from scrollphathd.fonts import font5x5, font5x7
from threading import Timer
from pypollen import Pollen
from clientsecrets import owmkey

owm = pyowm.OWM(owmkey)

# Lat and long here for where I live; replace as you wish.
latitude = 55.03973
longitude = -1.44713

interval = 15 * 60 # seconds between API data updates (15 mins)
showTime = 3  # seconds for each data display. 3 seconds feels about right.

BRIGHTNESS = 0.1 # the ScrollpHAT HD is insanely bright. This is enough, for me.
scrollphathd.rotate(degrees=180) # My unit is in a ScrollBot case. Which is upside-down

# Initialise our global variables with empty values
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

    # Save the old report

    oldReport = pressureReport

    try:
        # observation = owm.weather_at_place('Whitley Bay,GB')
        observation = owm.weather_at_id(2634032) # Prefer this approach if possible
        w = observation.get_weather()
        pressureReport = w.get_pressure()['press']
        # print("Pressure updated from API")
    except:
        # Something went wrong, reinstate the old value
        pressureReport = oldReport
    
    return pressureReport


def updatePollen():
    """Fetch pollen data from Benadryle / Met. Office.

    Triggered on a timer to avoid overloading API.
    """
    global pollenReport

    # Save the old report
    oldReport = pollenReport
    
    # re-initialise the string with a leading space, to avoid it
    # scrolling off the display immediately.
    pollenReport = " "
    # Alternate lines: the 5x7 font lacks lowercase letters,
    # so convert here ... or don't, accordingly.
    try:
        newReport = Pollen(latitude, longitude).pollencount
        pollenReport += newReport.upper()
    except:
        # Something went wrong, reinstate the old string
        pollenReport += oldReport

    pollenReport += "  "
    # print("Pollen updated from API")
    return pollenReport


def displayClock():
    """Documentation string.
    """

    timeString = time.strftime("%H:%M")
    # print(timeString)
    scrollphathd.clear()
    scrollphathd.write_string(timeString, font=font5x5, brightness=BRIGHTNESS)
    scrollphathd.show()
    time.sleep(showTime)


def displayPressure(startTime):
    """Documentation.
    """
    global showTime
    global pressureReport
    targetTime = startTime + showTime
    scrollphathd.clear()
    scrollphathd.write_string(str(pressureReport), font=font5x5, brightness=BRIGHTNESS)
    scrollphathd.show()    
    # print(pressureReport)    
        
    while (time.time() < targetTime):
        time.sleep(0.05)
    

def displayPollen(startTime):
    """Documentation.
    """
    global showTime
    global pollenReport
    targetTime = startTime + showTime
    scrollphathd.clear()
    scrollphathd.write_string(pollenReport, font=font5x5, brightness=BRIGHTNESS)
    # print(pollenReport)

    while (time.time() < targetTime):
        scrollphathd.show()
        scrollphathd.scroll()
        time.sleep(0.1)


if __name__ == "__main__":
    
    # Get data on initial start
    pressureReport = updatePressure()
    pollenReport = updatePollen()

    # Clear the screen
    scrollphathd.clear()

    # Start the data update timers, effectively on background threads
    rtPressure = RepeatedTimer(interval, updatePressure)
    rtPollen = RepeatedTimer(interval, updatePollen)

    # ...and now we can loop
    while True:
        displayClock()
        displayPressure(time.time())
        displayPollen(time.time())
        # ...and around we go again.
