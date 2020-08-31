'''
Copyright (C) 2020 Daniel Fitzgerald

"aa.py" is a useless temporary file with debug code.
'''

import urllib.request
import re

def downloadFile(url):
    with urllib.request.urlopen(url) as u:
        b = u.read()
    # TODO: Fix/verify hardcoded encoding if possible...
    return str(b, encoding='utf-8'), u.getcode()

sample_data = downloadFile('https://weather.gc.ca/wxlink/site_js/s0000001_e.js')[0]
import weatherstation
ws = weatherstation.WeatherStation(js=sample_data)
