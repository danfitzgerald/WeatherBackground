'''
Copyright (C) 2020 Daniel Fitzgerald

"processdata.py" processes data downloaded by "downloaddata.py". It extracts
a table of weather station names and their corresponding urls.
'''

import re
from downloaddata import DATASET_LOC
import os
import weatherstation


PROCESSED_DATA_LOC = 'dataset/city_prov_url.csv'


def load_file(location):
    file = open(location, mode='r')
    file_content = file.read()
    file.close()
    return file_content


'''
Extract weather station names.
'''
def extract_stations(raw_data):
    stations = []
    
    # Stations cities, provinces and urls are extracted using regualar expressions
    cities = re.findall('var cityName = "(.*)"', raw_data)
    provinces = re.findall('var provinceName = "(.*)"', raw_data)
    urls = re.findall('(.*)\\nEND', raw_data)
    
    for i in range(0, len(cities)):
        city = cities[i]
        province = provinces[i]
        url = urls[i]
        stations.append(weatherstation.WeatherStation(city, province, url))

    return stations


def main():
    # First test if output file already exists
    if os.path.isfile(PROCESSED_DATA_LOC):
        print("Processed data at %s already exists. If you wish to rebuild data"
              " delete the file at %s." % (PROCESSED_DATA_LOC, PROCESSED_DATA_LOC))
    elif not os.path.isfile(DATASET_LOC):
        print('File at %s does not exist. Raw data has not been downloaded from'
              ' weather.gc.ca. You must run "downloaddata.py" first.' % DATASET_LOC)
    else: # If tests pass
        raw_data = load_file(DATASET_LOC)
        stations = extract_stations(raw_data)
        csv = weatherstation.station_to_csv(stations)
        with open(PROCESSED_DATA_LOC, mode='w') as data_file:
            data_file.write(csv)


if __name__ == '__main__':
    main()
