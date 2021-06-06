import classes
import dataLoading

# make an object signal as an instance of class Signal
signal = classes.Signal()

# Use function to load signal from csv file
dataLoading.load_signal('rawGSR', signal)

# test to print
print(signal.sampledSignal)

# test to draw plot
dataLoading.draw_plot(signal.sampledSignal, 'GSR signal', 'Raw GSR signal', 'GSR value', 'TimeStamp')

