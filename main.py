import classes
import dataLoading
import dataProcessing
import configparser

# make an object signal as an instance of class Signal
signal = classes.Signal()

# Use function to load signal from csv file
signal.signalSamples = dataLoading.load_signal('rawGSR')

# Here we update vector with values of the si - test - gnal
signal.update_values()

# test to print
print(signal.signalSamples)

# test to draw plot FIZEMO-3
dataLoading.draw_plot(signal.signalSamples, 'GSR signal', 'Raw GSR signal', 'GSR value', 'TimeStamp')

# test to read config.ini file FIZEMO-4
configObject = configparser.ConfigParser()
configObject.read('config.ini')
decimationData = configObject['decimation_info']
samplingFrequency = decimationData['samplingFrequency']
goalFrequency = decimationData['goalFrequency']
print('Sampling frequency:', int(samplingFrequency), 'and goal frequency:', int(goalFrequency))

# test to decimate signal and plot it FIZEMO-5
signal.signalSamples = dataProcessing.decimation_process(signal.signalSamples, samplingFrequency, goalFrequency)
dataLoading.draw_plot(signal.signalSamples, 'GSR signal', 'Decimated GSR signal', 'GSR value', 'TimeStamp')

# Here we update vector with values of the signal after we have decimated it
signal.update_values()

