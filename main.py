import classes
import dataLoading
import configparser

# make an object signal as an instance of class Signal
signal = classes.Signal()

# Use function to load signal from csv file
dataLoading.load_signal('rawGSR', signal)

# test to print
print(signal.sampledSignal)

# test to draw plot FIZEMO-3
dataLoading.draw_plot(signal.sampledSignal, 'GSR signal', 'Raw GSR signal', 'GSR value', 'TimeStamp')

# test to read config.ini file FIZEMO-4
configObject = configparser.ConfigParser()
configObject.read('config.ini')
decimationData = configObject['decimation_info']
print('Sampling frequency:', int(decimationData['samplingFrequency']),
      'and decimation frequency:', int(decimationData['decimationFrequency']))

