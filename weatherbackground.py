'''
Copyright (C) 2020 Daniel Fitzgerald

"weatherbackground.py"
'''

import urllib.request
import re
import weatherstation
from processdata import PROCESSED_DATA_LOC

def download_http(url):
    with urllib.request.urlopen(url) as u:
        b = u.read()
    # TODO: Fix/verify hardcoded encoding if possible...
    return str(b, encoding='utf-8'), u.getcode()

def launch_interactive_console():
    with open(PROCESSED_DATA_LOC, mode='r') as f:
        directory = f.read()
    wxStations = weatherstation.csv_to_station(directory)
    
    print('Interactive console mode.')
    print('  1: Search by city')
    print('  2: Search by province')
    print('  0: Exit')
    choice = input('\nPlease enter a choice <number>: ')

    def print_station(station):
        data, status_code = download_http(station.getUrl())
        # TODO: Check status code
        station.applyJs(data)
        print('City:\t', station.getCity())
        print('Province:\t', station.getProvince())
        print(station.getUserFriendlyUrl())
        print('Temperature:\t%s deg C' % station.getTemperature())
        print('Wind speed (direction):\t' + station.getWindSpeed()
              + 'km/h (' + station.getWindDir() + ')')

    # Search by city.
    if choice == '1':
        query = input('Enter city name: ')
        results = weatherstation.search_for_station(wxStations, query)
        
        if len(results) == 0:
            print('No results.')
        if len(results) == 1:
            print_station(results[0])
        if len(results) > 1:
            for i in range(0, len(results)):
                result = results[i]
                print(str(i+1) + ': ' + result.getCity() + ', ' + result.getProvince())
            choice = int(input('\nEnter choice <number>: '))
            station = results[choice-1]
            print_station(station)
            
            
    elif choice == '0':
        return
    else:
        print('Invalid choice.')
        

def main():
    # To do check for if table of weather stations by city, province and url exists
    launch_interactive_console()


if __name__ == '__main__':
    main()
