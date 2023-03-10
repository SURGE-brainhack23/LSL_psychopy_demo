#This program streams data from the OpenBCI as a participant views a basic fixation and a grating stimulus
#The program stops reading data and switches stimuli when a key is pressed
#Basic processing of the signals is done to subtract the fixation response from the grating response
#This script shows some of the functionality of psychopy and how it can be integrated with OpenBCI data 

#imports
from pylsl import StreamInlet, resolve_stream
import numpy as np 
import time
import pandas as pd 
from psychopy import visual, core, event

#Set up some basic psychopy stimuli 
mywin = visual.Window([800,600], monitor="testMonitor", units="deg") #create a window
grating = visual.GratingStim(win=mywin, mask="circle", size=3, pos=[0,0], sf=3)
fixation = visual.GratingStim(win=mywin, size=0.5, pos=[0,0], sf=0, rgb=-1)

#Set these variables to specify what data you want to collect
epochLength = 0.5 #How often the code pulls data from the OpenBCI
numEpochs = 100 #How many times data is pulled (set to 100 but will exit earlier if key pressed)
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
raw = []       #creates an empty list for raw data 
data = np.zeros((1,numTargetChannels))

#Function to read in some data at specified intervals and save to a csv file
def readData(epochLength, numEpochs, epochTimes, raw, data, targetChannels, fileName, scale_fac_uVolts_per_count, chanNames):
    
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
            print(timestamp)
        
            if len(epoch)>0:    # This if-statement is here in case we grab an empty chunk (which seems to happen on the first call to pull_chunk)
                #appends data to list 
                
                epoch = np.array(epoch) * scale_fac_uVolts_per_count
                data = np.vstack((data, epoch[:,targetChannels]))
                
                #increment counter
                ctr = ctr+1 
            
            #You can also process the data in real time and save some summary metrics here!
            
            #check each loop to see if a key was pressed 
            if len(event.getKeys())>0:
                break
            event.clearEvents()
            
    return data

#Function to save recorded data
def saveData(data):
    #converts list to a pandas dataframe and writes data to a file 
    datArray = np.array(data)
    datArray = np.vstack(datArray)
    rawDf = pd.DataFrame(datArray, columns=chanNames)
    rawDf.to_csv(fileName)
    print(rawDf)

### MAIN ####

#draw a fixation (baseline) and update the window
fixation.draw()
mywin.update()
#Read data in a loop until key is pressed and then save data
baseline_data = readData(epochLength, numEpochs, epochTimes, raw, data, targetChannels, fileName, scale_fac_uVolts_per_count, chanNames)
saveData(baseline_data) 

#draw the stimuli and update the window
grating.draw()
mywin.update()
#Read data in a loop until key is pressed and then save data
grating_data = readData(epochLength, numEpochs, epochTimes, raw, data, targetChannels, fileName, scale_fac_uVolts_per_count, chanNames)
saveData(grating_data) 

#Do some processing to the data
#You may also want to do some frequency band filtering here (note: gamma activity in the visual cortex shows changes in response to a grating stimulus)
avg_baseline = np.mean(np.abs(baseline_data))
avg_grating = np.mean(np.abs(grating_data))
diff_activity = avg_grating - avg_baseline 

#Present something based on processing of data
#Here you can load in image files (e.g., happy face and sad face) and present them to provide the user 
#with feedback on their brain activity

#Resets to a fixation 
fixation.draw()
mywin.update()
core.wait(5.0)


