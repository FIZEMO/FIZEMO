import classes
import dataLoading
import dataProcessing
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
samplingFrequency = decimationData['samplingFrequency']
goalFrequency = decimationData['goalFrequency']
print('Sampling frequency:', int(samplingFrequency), 'and goal frequency:', int(goalFrequency))

# test to decimate signal and plot it FIZEMO-5
signal.decimatedSignal = dataProcessing.decimation_process(signal.sampledSignal, samplingFrequency, goalFrequency)
dataLoading.draw_plot(signal.decimatedSignal, 'GSR signal', 'Decimated GSR signal', 'GSR value', 'TimeStamp')

