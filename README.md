# DataBot

Simple hack to display a rotation of current time, current atmospheric pressure, and today's pollen forecast, on a Pimoroni ScrollpHAT HD display, attached to a Pi Zero.

As of 2019-04-23 there's no error handling on API update requests, so this won't necessarily be very roboust. But hey, it's worth a try.

Totals about 10% CPU on a Pi Zero W, with just this script running on a no-GUI Raspbian install. Initial RAM usage is about 50Mb.

## Installation

pip3 install required for:

    pyowm
    pypollen

Sign up for an OpenWeatherMap API key, add to `clientsecrets.py` file in project root:

    owmkey = '<key here>'

Also using PyPollen from Benadryl (!), which builds on the Met. Office's pollen forecast with arm-waving something something. However, the API is drop-dead simple.

Download to `~/DataBot` (assuming using `pi` user).

### Systemctl

See [Raspberry Pi docs](https://www.raspberrypi.org/documentation/linux/usage/systemd.md) for `systemctl` instructions; `.service` file provided, needs copying into `/etc/systemd/system/` and enabling (test with `start` first).
