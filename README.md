**Getting Started with OpenBCI and Python:**
**Lab Streaming Layer and Psychopy **

Resources: 

OpenBCI Documentation:
http://docs.openbci.com/OpenBCI%20Software/01-OpenBCI_GUI
https://github.com/OpenBCI/OpenBCI_Processing
Python documentation: 
https://docs.python.org/3/library/index.html
API for psychopy: 
http://www.psychopy.org/api/api.html
OpenBCI_LSL package: 
https://github.com/OpenBCI/OpenBCI_LSL
API for pylsl: 
https://github.com/sccn/labstreaminglayer
https://github.com/sccn/labstreaminglayer/blob/master/LSL/liblsl-Python/pylsl/pylsl.py
Command overview for setting up data stream:
https://github.com/OpenBCI/Docs/blob/master/OpenBCI%20Software/04-OpenBCI_Cyton_SDK.md

Setting up your computer  

In order to run the code, you must first complete these steps on the computer you plan to use to present the paradigm. 

OpenBCI_LSL setup:
1.	Download or clone the OpenBCI_LSL repository from Github: https://github.com/OpenBCI/OpenBCI_LSL

2.	Download and install python version 2 or 3: https://www.python.org/downloads/  

3.	Install pylsl and dependencies using conda: 

conda install -c conda-forge liblsl
	
If not all dependencies install, you can also install the following individually using 
conda install

a.	pyserial (version 3.1.1 or greater)
b.	numpy (version 1.11.1 or greater)
c.	pyqtgraph (version 0.9.10 or greater)
d.	scipy (version 0.17.1 or greater)


PsychoPy setup:
1.	Download and install the Standalone PsychoPy package appropriate to the system: https://www.psychopy.org/download.html

2.	The pylsl module (necessary for data streaming from the headset) may not automatically work with the standalone PsychoPy application and will need to first be moved to the appropriate directory to be used. 	
You will need to locate the current directory of the pylsl module and drag the folder titled ‘pylsl’ to the appropriate PsychoPy directory. You can do this with the following steps: 
a.	Open python or ipython and type the following:
import pylsl
print(pylsl.__file__)
		This will return a string with the location of your pylsl module
b.	Copy the directory up to the folder before ‘/pylsl/’. For example if the directory is:
/Users /.local/lib/python3.6/site-packages/pylsl/__init__.py
Copy: /Users/.local/lib/python3.6/site-packages
c.	Return to the command line terminal and type open followed by the directory you just copied. 
This will open a finder window where you will see a folder titled ‘pylsl’
d.	In a second finder window:
i.	Go to ‘Applications’
ii.	Right click on the PsychoPy application and click show package contents
iii.	Navigate to Contents/Resources/lib/python3.8
e.	Drag and drop the ‘pylsl’ folder into this directory 

Note: if you have trouble importing any other external modules into PsychoPy you can repeat this process. 

You should now be set up to run the PsychoPy paradigm on your computer. 

Streaming Data:

To start the stream, plug the dongle in to the USB port and turn on the BCI board (switch to “PC”). Then open a terminal window and type the following commands:
•	cd <directory to the ‘OpenBCI_LSL-master’ folder>
•	python openbci_lsl.py –stream
•	x1060101Xx2060101Xx3060101Xx4060101Xx5060101Xx6060101Xx7060101Xx8060101X 
•	/start

Note: the long string of numbers will configure the openBCI with the following settings: 
•	Power: On 
•	Gain: 24
•	Input type: Normal
•	Bias: Remove from bias 
•	SRB2: disconnect
•	SRB1: connect 

This will start the data stream from the OpenBCI headset, and you can then launch the PsychoPy Coder.


PsychoPy Code:

There are 2 PsychoPy scripts to help get you started with your project:
1.	OpenBCI_readAndSave:
•	This program simply reads in data from the OpenBCI at specified intervals, concatenates the data, and saves it to a csv for offline processing.
•	There is no stimuli presentation or BCI implementation in this script. 
•	The expected output is a list of timestamps and a print-out of the final dataframe to confirm that the data is streaming correctly.
2.	OpenBCI_stimulusDemo: 
•	This program streams data from the OpenBCI as a participant views a basic fixation and a grating stimulus.
•	The program stops reading data and switches stimuli when a key is pressed.
•	Basic processing of the signals is done to subtract the fixation response from the grating response.
•	This script shows some of the functionality of psychopy and how it can be integrated with OpenBCI data.
![image](https://user-images.githubusercontent.com/25189351/224364690-74afb27f-c401-4c97-ba03-8c35ec9413dd.png)
