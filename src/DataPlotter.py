'''
Created on 2014-08-08

@author: Martin
'''

try:
    import os, traceback
    from src.OscilloscopeParser import loadDataFromFile
    import matplotlib.pyplot as plt
    import matplotlib as mpl
    from matplotlib.widgets import Slider
    import numpy as np
except:
    print traceback.format_exc()
    raw_input('Press Enter to close')

DATA_DIRECTORY = os.path.join("..", "Data")

DATA_FOLDER = 'NEW_FOLD'
plotIndexNum = 1

def setAxisToColor(axis, color):
    plt.setp(axis.spines.values(), color=color)
    plt.setp([axis.get_xticklines(), axis.get_yticklines()], color=color)

if __name__ == '__main__':
    oscilloscopeDataList = loadDataFromFile(os.path.join(DATA_DIRECTORY, DATA_FOLDER))
    pairedData = list()
    for oscilloscopeData in oscilloscopeDataList:
        dataNum = int(os.path.splitext(oscilloscopeData.getFilename())[0][-4:])
        if(dataNum % 2 == 0):
            dataA = oscilloscopeData
        else:
            dataB = oscilloscopeData
            pairedData.append((dataA, dataB))
    plotData = pairedData[plotIndexNum]
    fig, ax1 = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.2)
    dataA = plotData[0].getData()
    ax1.scatter(np.linspace(plotData[0].dataStartTime, plotData[0].dataEndTime, num=plotData[0].recordLength, endpoint=True), dataA, color=u'r', marker=u'.')
    setAxisToColor(ax1, u'r')
    ax1.set_xlim(plotData[0].dataStartTime, plotData[0].dataEndTime)
    ax1.set_ylabel('plot 1')
    ax2 = ax1.twiny()
    dataB = plotData[1].getData()
    ax2.scatter(np.linspace(plotData[1].dataStartTime, plotData[1].dataEndTime, num=plotData[1].recordLength, endpoint=True), dataB, color=u'b', marker=u'.')
    setAxisToColor(ax2, u'b')
    axslide = plt.axes([0.1, 0.1, 0.8, 0.03])
    width = plotData[0].sampleInterval * plotData[0].recordLength
    slider = Slider(axslide, "shifter", -width, width, valinit=0.0)
    def sliderUpdate(val):
        ax2.set_xlim(-val+plotData[1].dataStartTime, -val +plotData[1].dataStartTime+ width)
    slider.on_changed(sliderUpdate)
    plt.show()
