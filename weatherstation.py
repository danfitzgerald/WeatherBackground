'''
Copyright (C) 2020 Daniel Fitzgerald

"weatherstation.py" stores, encodes, and decodes weather data.
'''


import re


class WeatherStation:
    """
    An abstract object to make dealing with weather stations easier
    to understand.
    """

    def __init__(self, city=None, province=None, url=None, js=None):
        """
        WeatherStation accepts either a combination of
        city, province and url inputs or js as an input.
        Any other combination of arguments will cause the object
        to be inoperable, or not operate as intended.
        """
        if city and province and url:
            self._city = city
            self._province = province
            self._url = url
        elif js:
            self._url = url
            self.applyJs(js)

    # Getters
    def getCity(self):
        return self._city
    def getProvince(self):
        return self._province
    def getUrl(self):
        return self._url

    def getJs(self):
        return self._js
    def getTemperature(self):
        return self._temperature
    def getWindSpeed(self):
        return self._windSpeed
    def getWindDir(self):
        return self._windDir
    def getUserFriendlyUrl(self):
        return self._userFriendlyUrl

    def applyJs(self, js):
        self._js = js
        self._city = None
        self._province = None
        self._temperature = None
        self._windDir = None
        self._windSpeed = None
        self._userFriendlyUrl = None
        
        def findRe(exp, s):
            m = re.findall(exp, s)
            if len(m) > 0: return m[0]
            else: return None
                
        for line in js.split('\n'):
            if self._city == None:
                m = findRe('var cityName = "(.*)"', line)
                if not m == None:
                    self._city = m
            if self._province == None:
                m = findRe('var provinceName = "(.*)"', line)
                if not m == None:
                    self._province = m
            if self._temperature == None:
                m = findRe('var obTemperature = "(.*)"', line)
                if not m == None:
                    self._temperature = m
            if self._windDir == None:
                m = findRe('var obWindDir = "(.*)"', line)
                if not m == None:
                    self._windDir = m
            if self._windSpeed == None:
                m = findRe('var obWindSpeed = "(.*)"', line)
                if not m == None:
                    self._windSpeed = m
            if self._userFriendlyUrl == None:
                m = findRe('var cityURL = "(.*)"', line)
                if not m == None:
                    self._userFriendlyUrl = m

    def getCsvRow(self):
        return self.getCity() + ',' + self.getProvince() + ',' + self.getUrl()
    
    def __str__(self):
        return "'(WeatherStation object): " + self.getCity() + ', ' + self.getProvince() + "'"
    def __repr__(self):
        return self.__str__()


'''
Takes in a list of WeatherStations and returns the data as a string in csv format.
'''
def station_to_csv(stations):
    csv = ''
    for station in stations:
        if csv == '':
            csv = station.getCsvRow()
        else:
            csv += '\n' + station.getCsvRow()
    return csv

'''
Takes in a string in csv format and returns WeatherStations.
'''
def csv_to_station(csv_data):
    csv_rows = csv_data.split('\n')
    stations = []
    for row in csv_rows:
        elements = row.split(',')
        city = elements[0]
        prov = elements[1]
        url = elements[2]
        station = WeatherStation(city, prov, url)
        stations.append(station)
    return stations

def search_for_station(wxStations, city):
    stations = []
    # Linear search for station
    for station in wxStations:
        if city.upper() == station.getCity().upper():
            return [station]
        elif city.upper() in station.getCity().upper():
            stations.append(station)
    return stations
