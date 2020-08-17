'''
Copyright 2020 Daniel Fitzgerald

"downloaddata.py" downloads all forcasts for all weather stations in Canada.
Its purpose is to download the forecasts in .js format and exctract Weather station
locations and produce a list of all weather stations in Canada with their corresponding
urls. It may also be used to download current conditions in parts of Canada to be
analysed etc...
'''

import urllib.request
from urllib.error import URLError

DATASET_LOC = "dataset/unprocessed_pages.txt"
FAILURE_ATTEMPTS = 15 # Number of times to skip pages that return 404.

def main():
    lead_url = 'https://weather.gc.ca/wxlink/site_js/s'
    digit_len = 7
    trail_url = '_e.js'

    page_counter = 1

    def build_url(counter):
        counter = str(counter).zfill(digit_len)
        return lead_url + counter + trail_url

    # Open datafile destination.
    f = open(DATASET_LOC, mode='ab')
    f.seek(0, 0)
    f.truncate()

    # Make initial request.
    url = build_url(page_counter)
    try:
        u = urllib.request.urlopen(url)
    except URLError as err:
        status_code = err.code
    else:
        b = u.read()
        status_code = u.getcode()
        f.write(b)
        f.write(b'\n%s\nEND\n' % bytes(u.geturl(), 'utf-8'))
        print(page_counter)
        u.close()

    # Some numbers are skipped (possibly removed weather stations?).
    # Therefore, we must have a tolerance for 404 responses until program terminates.
    remaining_attempts = FAILURE_ATTEMPTS
    if not status_code == 200:
        remaining_attempts -= 1
        print('Failed attempt status_code: %d, url: %s' % (status_code, url))

    while remaining_attempts > 0:
        page_counter += 1
        url = build_url(page_counter)

        try:
            u = urllib.request.urlopen(url)
        except URLError as err:
            status_code = err.code
        else:
            b = u.read()
            status_code = u.getcode()
            f.write(b)
            f.write(b'\n%s\nEND\n' % bytes(url, 'utf-8'))
            print(page_counter)
            u.close()
            
        if status_code == 200:
            remaining_attempts = FAILURE_ATTEMPTS
        else:
            remaining_attempts -= 1
            print('Failed attempt status_code: %d, url: %s' % (status_code, url))

    f.write(b'\nEOF')
    f.close()

    print('Completed with final page status code: %d, url: %s' % (status_code, url))

if __name__ == '__main__':
    main()
