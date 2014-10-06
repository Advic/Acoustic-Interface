'''
Created on 2014-09-03

@author: Martin
'''
from src.OscilloscopeParser import OscilloscopeData

try:
    import os, traceback
    from src.OscilloscopeParser import loadDataFromFile
    import numpy as np
except:
    print traceback.format_exc()
    raw_input('Press Enter to close')

DATA_DIRECTORY = os.path.join("..", "Data")

def calculateDotProduct(oscilloscopeDataA, oscilloscopeDataB, indexshift):
    dotSum = 0
    dataB = oscilloscopeDataB.getData()
    for indexA, valA in enumerate(oscilloscopeDataA.getData()):
        if(0 < indexA + indexshift < len(dataB)):
            valB = dataB[indexA + indexshift]
            dotSum += valA * valB
    return dotSum

if __name__ == '__main__':
    oscilloscopeDataList = loadDataFromFile(os.path.join(DATA_DIRECTORY, 'NEW_FOLD'))
    pairedData = list()
    for oscilloscopeData in oscilloscopeDataList:
        dataNum = int(os.path.splitext(oscilloscopeData.getFilename())[0][-4:])
        if(dataNum % 2 == 0):
            dataA = oscilloscopeData
        else:
            dataB = oscilloscopeData
            pairedData.append((dataA, dataB))
    pairedDataDotProducts = list()
    for (oscilloscopeDataA, oscilloscopeDataB) in pairedData:
        print "working on", oscilloscopeDataA.getFilename()
        assert oscilloscopeDataA.dataStartTime == oscilloscopeDataB.dataStartTime
        assert oscilloscopeDataA.sampleInterval == oscilloscopeDataB.sampleInterval
        assert oscilloscopeDataA.recordLength == oscilloscopeDataB.recordLength
        pairedDataDotProducts.append([calculateDotProduct(oscilloscopeDataA, oscilloscopeDataB, index) for index in range(-oscilloscopeDataA.recordLength, oscilloscopeDataA.recordLength)])
    print pairedDataDotProducts