'''
Copyright 2020 Daniel Fitzgerald

"processdata.py" processes data downloaded by "downloaddata.py". It extracts
a table of weather station names and their corresponding urls.
'''

import re
from downloaddata import DATASET_LOC


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
        stations.append(WeatherStation(city, province, url))

    return stations


# Setup an abstract object to make dealing with weather stations easier
# to understand.
class WeatherStation:
    def __init__(self, city, province, url):
        self._city = city
        self._province = province
        self._url = url

    def getCity(self):
        return self._city
    def getProvince(self):
        return self._province
    def getUrl(self):
        return self._url
    def getCsvRow(self):
        return self.getCity() + ',' + self.getProvince() + ',' + self.getUrl()
    def __str__(self):
        return "'" + self.getCity() + ', ' + self.getProvince() + ', ' + self.getUrl() + "'"
    def __repr__(self):
        return self.__str__()


def generate_csv(stations):
    csv = ''
    for station in stations:
        if csv == '':
            csv = station.getCsvRow()
        else:
            csv += '\n' + station.getCsvRow()
    return csv


def main():
    raw_data = load_file(DATASET_LOC)
    stations = extract_stations(raw_data)
    # todo: save csv data
    print(generate_csv(stations))


if __name__ == '__main__':
    main()
