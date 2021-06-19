import scipy.signal as ss
from matplotlib import pyplot as plt
import pandas as pd


# Class for main signal
#  - signalSamples: two-dimensions list with signal [[timestamps, values]]

class Signal:

    # Initialization of signal object
    #   Loading signal from .csv file and save it as signalSamples property
    #       - first argument name of the .csv file placed in folder ./signals
    def __init__(self, fileName):
        path = './signals/' + fileName + '.csv'
        pandasDataFramedSignal = pd.read_csv(r'' + path)
        self.signalSamples = pandasDataFramedSignal.to_numpy()

    # Function for signal decimation
    # - first argument is dictionary with attributes, where:
        # "samplingFrequency" is frequency with which signal was sampled
        # "goalFrequency" is goal frequency with which signal should be sampled
    def decimate(self, attr):
        ratio = int(int(attr["samplingFrequency"]) / int(attr["goalFrequency"]))
        self.signalSamples = ss.decimate(self.signalSamples, ratio, 8, axis=0)

    # Function to draw plot from given data
    # - first argument is a name of the window
    # - second argument is a title of the plot
    # - third argument is a name of X axis
    # - fourth argument is a name of Y axis
    def draw_plot(self, windowName, titleName, xName, yName):
        x_axis, y_axis = zip(*self.signalSamples)
        plt.figure(windowName)
        plt.title(titleName)
        plt.xlabel(xName)
        plt.ylabel(yName)
        plt.plot(x_axis, y_axis)
        plt.show()
