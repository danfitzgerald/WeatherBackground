'''
An abstract object to make dealing with weather stations easier
to understand.
'''
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