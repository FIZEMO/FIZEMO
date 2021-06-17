import classes
import configparser

# make an object signal as an instance of class Signal
signal = classes.Signal('rawGSR')
signal.draw_plot('GSR signal', 'Raw GSR signal', 'GSR value', 'TimeStamp')


# test to read config.ini file
configObject = configparser.ConfigParser()
configObject.read('config.ini')
decimationData = configObject['decimation_info']
samplingFrequency = decimationData['samplingFrequency']
goalFrequency = decimationData['goalFrequency']
print('Sampling frequency:', int(samplingFrequency), 'and goal frequency:', int(goalFrequency))

signal.decimate(samplingFrequency, goalFrequency)
signal.draw_plot('GSR signal', 'Decimated GSR signal', 'GSR value', 'TimeStamp')

class_method = getattr(signal, "decimate")
class_method(samplingFrequency, goalFrequency)

