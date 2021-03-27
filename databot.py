"""DataBot - display atmospheric pressure on a Pimoroni ScrollBot.
"""

import pyowm
import time
import scrollphathd
from scrollphathd.fonts import font5x5, font5x7
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

interval = 30 * 60 # seconds between API data updates (30 mins)
showTime = 3  # seconds for each data display. 3 seconds feels about right.

BRIGHTNESS = 0.1 # the ScrollpHAT HD is insanely bright. This is enough, for me.
scrollphathd.rotate(degrees=180) # My unit is in a ScrollBot case. Which is upside-down

# Initialise our variables as globals, with empty values
pressureReport = 0
pollenReport = "NAN"
tempReport = 0.0

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
    - 2019-07-28 Also update daily max. temperature
    - 2021-03-27 Fixes for PyOWM 3
    """
    global pressureReport, tempReport, mgr

    # Save the old report
    oldReport = pressureReport
    oldTempReport = tempReport

    try:
        # observation = owm.weather_at_place('Whitley Bay,GB')
        observation = mgr.weather_at_id(2634032) # Prefer this approach if possible
        # w = observation.get_weather()
        pressureReport = observation.weather.pressure["press"]
        tempReport = observation.weather.temperature('celsius')['temp']
        print("Pressure updated from API")
    except:
        # Something went wrong, reinstate the old value
        print(">>> Pressure error")
        pressureReport = oldReport
        tempReport = oldTempReport

    return pressureReport


def updatePollen():
    """Fetch pollen data by scraping Met. Office website.

    Triggered on a timer to avoid overloading site.
    Now scraping web data instead of using pypollen, since that was
    unreliable. Hard-coded to North-East region ('ne').
    """

    global pollenReport

    # Save the old report
    # Disabled for visible error reporting
    # oldReport = pollenReport

    # re-initialise the string with a leading space, to avoid it
    # scrolling off the display immediately.
    pollenReport = " "

    # Alternate lines: the 5x7 font lacks lowercase letters,
    # so convert here ... or don't, accordingly.
    try:
        # Get the web page as a pyquery object
        newReport = pq(url="https://www.metoffice.gov.uk/weather/warnings-and-advice/seasonal-advice/pollen-forecast")
        # Drop into the HTML for the first results table for North-East
        myReport = newReport("#ne table tbody tr td div span")
        # Get the text representation of that element.
        myReportText = myReport.html()

        # Step through possible outcomes
        if myReportText == "L":
            pollenReport = " LOW "
        elif myReportText == "M":
            pollenReport = " MODERATE "
        elif myReportText == "H":
            pollenReport = " HIGH "
        elif myReportText == "VH":
            pollenReport = " VERY HIGH "
        elif myReportText == "None":
            pollenReport - " NO POLLEN "
        else:
            # Not sure of other codes, so just display the raw string
            pollenReport = myReportText
    except:
        # Something went wrong, display error
        pollenReport = " POLLEN ERROR "
        raise RuntimeError('Pollen scraping error')
        # Something went wrong, reinstate the old string
        # pollenReport += oldReport

    print("Pollen updated from API")
    return pollenReport


def displayClock():
    """Render current time to the ScrollpHAT."""

    global showTime
    # Get the current time
    timeString = time.strftime("%H:%M")
    print(timeString)
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
    print(pressureReport)

    while (time.time() < targetTime):
        time.sleep(0.05)

    scrollphathd.clear()
    scrollphathd.write_string(str(tempReport), font=font5x5, brightness=BRIGHTNESS)
    scrollphathd.show()

    targetTime = time.time() + showTime

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
