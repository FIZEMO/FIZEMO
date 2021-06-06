import classes
import dataLoading

# make an object signal as an instance of class Signal
signal = classes.Signal()

# Use function to load signal from csv file
dataLoading.load_signal('signal_GSR', signal)

# test to print
print(signal.sampledSignal)
