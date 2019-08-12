"""Parsing test for pollen data from web source.

Uses PyQuery to parse HTML.

    pip3 install pyquery

(relies on LXML, which is a C dependency, but so it goes)

"""

from pyquery import PyQuery as pq

# d = pq(url='')
#d = pq(filename="/Users/jonathan/Documents/GitHub/DataBot/experiments/sample-pollen-forecast.html")

d = pq(url="https://www.metoffice.gov.uk/weather/warnings-and-advice/seasonal-advice/pollen-forecast")

# What we're after is:
#ne > table > tbody > tr > td:nth-child(1) > div > span

p = d("#ne table tbody tr td div span")
print(p.html())

# Should output 'L' or 'M' or 