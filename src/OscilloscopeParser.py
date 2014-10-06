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
    #===========================================================================
    # @param directory: directory containing this file (for grouping)
    # @param filename: filnemae containing this data
    # @param propertyMap: dictionary of file properties, keyed on the property
    #    name (leftmost column of the oscilloscope data files)
    # @param data: dict of values keyed on the time at which that value was recorded
    # @param timedelta: time difference between two points of data
    #===========================================================================
    def __init__(self, directory, filename, propertyMap, data, starttime):
        self.__directory = directory
        self.__filename = filename
        self.__property_map = propertyMap
        self.__data = data
        self.__starttime = starttime

    @property
    def dataStartTime(self):
        return self.__starttime

    @property
    def dataEndTime(self):
        return self.__starttime + self.sampleInterval * (self.recordLength - 1)

    @property
    def sampleInterval(self):
        return self.getProperty("Sample Interval")

    @property
    def recordLength(self):
        return int(self.getProperty("Record Length"))

    def getDirectory(self):
        return self.__directory

    def getFilename(self):
        return self.__filename

    def getProperty(self, propertyName):
        return self.__property_map[propertyName]

    def getData(self):
        return self.__data

class OscilloscopePair():
#==============================================================================
# @param a,b: OscilloscopeData objects
#==============================================================================
    def __init__(self, a, b):
        self.__a = a
        self.__b = b

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

#===============================================================================
# @param dir: Full path of the directory ocntaining the Acoustic-Interface Data/
#        default is ..\Data
# @return: A list of OscilloscopeData objects (one for each file)
#===============================================================================
def loadDataFromFile(dir):
    data = list()
    for dataFile in os.listdir(dir):
        if os.path.splitext(dataFile)[-1] != '.csv':
            pass
        with open(os.path.join(dir, dataFile)) as csvfile:
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
        data.append(OscilloscopeData(dir, dataFile, properties, voltages, times[0]))
    return data

if __name__ == '__main__':
    DATA_DIRECTORY = os.path.join("..", "Data")
    for dataFolder in os.listdir(DATA_DIRECTORY):
        loadDataFromFile(os.path.join(DATA_DIRECTORY, dataFolder))
