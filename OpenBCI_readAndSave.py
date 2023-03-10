# This program reads in data from the OpenBCI at specified intervals, concatenates the data, 
# and saves data to a csv for offline processing.
# There is no stimuli presentation or BCI implementation in this script. 
# The expected output is a list of timestamps and a print-out of the final dataframe to confirm that 
# the data is streaming correctly. 

#imports
from pylsl import StreamInlet, resolve_stream
import numpy as np 
import time
import pandas as pd 

#Set these variables to specify what data you want to collect
epochLength = 0.1 #How often the code pulls data from the OpenBCI
numEpochs = 10 #How many times data is pulled
targetChannels = [0,1,2,3] #Channels you are interested in (numbers 0 through 7)
chanNames = ['chan1','chan2','chan3','chan4'] #Names of the channels (how you want them to save in your dataframe)
fileName = 'raw_data.csv' #Output data file for offline analysis 

# Access data stream
streams = resolve_stream('type', 'EEG')
inlet = StreamInlet(streams[0])
sfreq = streams[0].nominal_srate()
numChannels = streams[0].channel_count()

# OpenBCI Parameters
ADS1299_Vref = 4.5                                                                  #reference voltage for ADC in ADS1299.  set by its hardware
ADS1299_gain = 24.0                                                                 #assumed gain setting for ADS1299.  set by its Arduino code
scale_fac_uVolts_per_count = ADS1299_Vref/float((pow(2,23)-1))/ADS1299_gain*1000000.
scale_fac_accel_G_per_count = 0.002 /(pow(2,4))                                     #assume set to +/4G, so 2 mG 

#Data collection parameters
numTargetChannels = len(targetChannels)
epochTimes = []
data = np.zeros((1,numTargetChannels))

#Function to read in some data at specified intervals and save to a csv file
def readData(epochLength, numEpochs, epochTimes, data, targetChannels, fileName, scale_fac_uVolts_per_count, chanNames):
    
    #parameters for data reading loop
    ctr = 0
    startTime = time.time()
    loopStartTime = time.time()
    
    while ctr < numEpochs:
        #loops through once for every epoch
        if (time.time()-loopStartTime > epochLength):
            loopStartTime = time.time()
            epochTimes.append(loopStartTime)
            epoch, timestamp = inlet.pull_chunk()
        
            if len(epoch)>0:    # This if-statement is here in case we grab an empty chunk (which seems to happen on the first call to pull_chunk)
                #appends data to list 
                
                epoch = np.array(epoch) * scale_fac_uVolts_per_count
                data = np.vstack((data, epoch[:,targetChannels]))
                
                #increment counter
                ctr = ctr+1 
            
    #converts list to a pandas dataframe and writes data to a file 
    datArray = np.array(data)
    datArray = np.vstack(datArray)
    rawDf = pd.DataFrame(datArray, columns=chanNames)
    rawDf.to_csv(fileName)
    print(rawDf)

##Call data reading function## 
readData(epochLength, numEpochs, epochTimes, data, targetChannels, fileName, scale_fac_uVolts_per_count, chanNames)
