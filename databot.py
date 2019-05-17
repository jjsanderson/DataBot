"""DataBot - display atmospheric pressure on a Pimoroni ScrollBot.
"""

import pyowm
import time
import scrollphathd
from scrollphathd.fonts import font5x5, font5x7
from threading import Timer
from pypollen import Pollen
from clientsecrets import owmkey

# You'll need an Open Weather Map API key, stored in a clientsecrets.py file:
# owmkey = 'you_key_here'
# OWM query object here as a global, because I'm lazy.
owm = pyowm.OWM(owmkey)

# Lat and long for where I live; replace as you wish.
latitude = 55.03973
longitude = -1.44713

interval = 30 * 60 # seconds between API data updates (30 mins)
showTime = 3  # seconds for each data display. 3 seconds feels about right.

BRIGHTNESS = 0.1 # the ScrollpHAT HD is insanely bright. This is enough, for me.
scrollphathd.rotate(degrees=180) # My unit is in a ScrollBot case. Which is upside-down

# Initialise our variables as globals, with empty values
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
    """Fetch pollen data from Benadryl / Met. Office.

    Triggered on a timer to avoid overloading API.
    This is currently hacky because the API unstable, failing silently for
    extended periods. I'm trying to debug, but suspect I'll have to 
    scrape web page data instead.
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
        # If we're still here, we must have a new report
        # ...so rewrite the global
        # Call .upper because ScrollpHAT HD only has u/c characters in some fonts
        pollenReport = " " + newReport.upper() + " "
        # pollenReport += newReport.upper()
    except:
        # Something went wrong, display error
        pollenReport = " POLLEN ERROR "
        raise RuntimeError('Pollen API error')
        # Something went wrong, reinstate the old string
        # pollenReport += oldReport

    # pollenReport += "  "
    # print("Pollen updated from API")
    return pollenReport


def displayClock():
    """Render current time to the ScrollpHAT."""
    
    global showTime
    # Get the current time
    timeString = time.strftime("%H:%M")
    # print(timeString)
    scrollphathd.clear()
    scrollphathd.write_string(timeString, font=font5x5, brightness=BRIGHTNESS)
    scrollphathd.show()
    time.sleep(showTime)


def displayPressure(startTime):
    """Render pressure data to the ScrollpHAT."""
    
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
    """Render pollen data to the ScrrollpHAT."""
    
    global showTime
    global pollenReport
    targetTime = startTime + showTime
    scrollphathd.clear()
    scrollphathd.write_string(pollenReport, font=font5x5, brightness=BRIGHTNESS)
    # print(pollenReport)

    while (time.time() < targetTime):
        scrollphathd.show()
        # Some strings will be too long to display, so scroll laterally
        scrollphathd.scroll()
        time.sleep(0.075)


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
