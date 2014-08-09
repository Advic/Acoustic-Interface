'''
Created on 2014-08-07

@author: Zendai

Class to cut incoming data into segments of interest
'''

try:
    import traceback
    import os
    import csv
    import numpy as np
except ImportError, err:
    print traceback.format_exc()
    raw_input('Press Enter to close')
	
	
	
def identifySignal(data, threshold):
	"""Looks through the data to find sections that can be considered noise or signal.
Returns a set pairs notifying the end of a segment and whether it's data or not.
This should be used after filtering."""
	leftindex = 0
	rightindex = 0
	keys = []
	marker = []
	while True:
		try:
			leftindex = rightindex+1
			rightindex = data.index(0, leftindex)
			keys.append(rightindex)
			totalsignal = sum(data[leftindex:rightindex])
			if totalsignal < threshold*(rightindex-leftindex+1):
				marker.append(0)
			else:
				marker.append(1)
		except:
			keys.append(len(data))
			marker.append(0)
			break
	return zip(keys,marker)
    
if __name__ == '__main__':
    dat = [0,0,0,0.1,0.2,0.3,2,3,4,5,2,23,4,5,2,0,1,23,3,0,0.2,0.4,0.4]
    result = identifySignal(dat, 1)
