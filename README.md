# DataBot

Simple hack to display a rotation of current time, current atmospheric pressure, and today's pollen forecast, on a [Pimoroni ScrollpHAT HD](https://shop.pimoroni.com/products/scroll-phat-hd) display, attached to a [Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/).

As of 2019-05-17 there's minimal error handling on API update requests, so this won't necessarily be very roboust. But it mostly works in my testing – though see below for pollen count issue.

Totals about 10% CPU on a Pi Zero W, with just this script running on a no-GUI Raspbian install. Initial RAM usage is about 50Mb for the whole system.

## Installation

pip3 install required for:

    pyowm
    pyquery

apt install required for:

    sudo apt-get install libxslt-dev

(lxml install with pyquery is partly broken on Raspbian Stretch, misses this library.)

Sign up for an OpenWeatherMap API key, add to `clientsecrets.py` file in project root:

    owmkey = '<key here>'

Also using the [Benadryl Social Pollen Count](https://www.benadryl.co.uk/social-pollen-count)(!), which builds on the Met. Office's pollen forecast with arm-waving something something. However, the API is drop-dead simple using the pypollen module.

Download to `~/DataBot` (assuming using `pi` user).

### Systemctl

See [Raspberry Pi docs](https://www.raspberrypi.org/documentation/linux/usage/systemd.md) for `systemctl` instructions; `.service` file provided, needs copying into `/etc/systemd/system/` and enabling (test with `start` first).

## Issues

As of 2019-05-17 updates using the PyPollen library to query the Benadryl site is flaky. I'm seeing some API errors, some slow updates, and some silent failures. From 2019-08-11 a revised UpdatePollen method scrapes the Met Office website directly and parses it using [PyQuery](https://pythonhosted.org/pyquery/).

2020-06-23: Updated to allow for 'Very High' pollen reports, which somehow I'd missed last year.

### Worth doing at some point

* Refactor this code to be a bit less ridiculous with global variables. That is: actually return variables sensibly. This is a bit tricky with the update jobs running as background threads, though, and that seems neater than hard-coding updates into the main loop. Maybe the main loop should handle API calls and the background thread should cycle the display? Or mumble mumble classes and objects mumble?

