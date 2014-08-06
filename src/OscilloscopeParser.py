'''
Created on 2014-08-06

@author: Martin

This class parses data files generated saved as csv files by the (@todo: note
oscilloscope model) into OscilloscopeData objects.
'''

try:
    import traceback
    import os
    import csv
    import numpy as np
except ImportError, err:
    print traceback.format_exc()
    raw_input('Press Enter to close')

class DataPoint():
    def __init__(self, time, data):
        self.__time = time
        self.__data = data

class OscilloscopeData():
    def __init__(self, directory, filename, propertyMap, data):
        self.__directory = directory
        self.__filename = filename
        self.__property_map = propertyMap
        self.__data = data

    def getProperty(self, propertyName):
        return self.__property_map[propertyName]

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def loadDataFromFile(dir):
    data = list()
    for dataFolder in os.listdir(dir):
        for dataFile in os.listdir(dir + os.path.sep + dataFolder):
            with open(os.path.join(dir, dataFolder, dataFile)) as csvfile:
                csvreader = csv.reader(csvfile, skipinitialspace=True)
                csvdata = list()
                for row in csvreader:
                    csvdata.append(row)
            nptranspose = np.transpose(csvdata)
            property_keys = nptranspose[0]
            property_values = [float(e) if isfloat(e) else e for e in nptranspose[1]]
            properties = dict([entry for entry in zip(property_keys, property_values) if entry[0] != str()])
            times = [float(time) for time in nptranspose[3]]
            voltages = [float(voltage) for voltage in nptranspose[4]]
            timevoltage = zip(times, voltages)
            data.append(OscilloscopeData(dataFolder, dataFile, properties, timevoltage))

if __name__ == '__main__':
    DATA_DIRECTORY = os.path.join("..", "Data")
    loadDataFromFile(DATA_DIRECTORY)
