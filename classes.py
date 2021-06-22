import scipy.signal as ss
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stat


# Class for main signal
#  - signalSamples: two-dimensions list with signal [[timestamps, values]]
#  - features: two-dimensions list with extracted features [[name of the feature, value]]

class Signal:

    # Initialization of signal object
    #   Loading signal from .csv file and save it as signalSamples property
    #       - first argument name of the .csv file placed in folder ./signals
    def __init__(self, fileName):
        path = './signals/' + fileName + '.csv'
        pandasDataFramedSignal = pd.read_csv(r'' + path)
        self.signalSamples = pandasDataFramedSignal.to_numpy()
        self.features = []

    # Function for signal decimation
    # - first argument is dictionary with attributes, where:
    # "samplingFrequency" is frequency with which signal was sampled
    # "goalFrequency" is goal frequency with which signal should be sampled
    def decimate(self, attr):
        ratio = int(int(attr["samplingFrequency"]) / int(attr["goalFrequency"]))
        self.signalSamples = ss.decimate(self.signalSamples, ratio, 8, axis=0)

    # Function for signal decimation
    # - first argument is dictionary with attributes, where:
    # "samplingFrequency" is frequency with which signal was sampled
    # "goalFrequency" is goal frequency with which signal should be sampled
    def z_normalize(self):
        mean = np.mean(self.get_values())
        variance = np.var(self.get_values())

        for i, (timestamps, values) in enumerate(self.signalSamples):
            values = (values - mean)/variance
            self.signalSamples[i][1] = values


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

    # Function to extract mean value from the signal
    # After being extracted values are being saved to the features list.
    def mean(self, attr):
        value = np.mean(self.get_values())
        if not attr:
            self.features.append(["Mean", value])
        else:
            self.features.append([attr, value])

    # Function to extract median value from the signal
    # After being extracted values are being saved to the features list.
    def median(self, attr):
        value = np.median(self.get_values())
        if not attr:
            self.features.append(["Median", value])
        else:
            self.features.append([attr, value])

    # Function to extract standard deviation value from the signal
    # After being extracted values are being saved to the features list.
    def standard_deviation(self, attr):
        value = np.std(self.get_values())
        if not attr:
            self.features.append(["Standard_deviation", value])
        else:
            self.features.append([attr, value])

    # Function to extract minimum value from the signal
    # After being extracted values are being saved to the features list.
    def minimum(self, attr):
        value = np.min(self.get_values())
        if not attr:
            self.features.append(["Minimum", value])
        else:
            self.features.append([attr, value])

    # Function to extract maximum value from the signal
    # After being extracted values are being saved to the features list.
    def maximum(self, attr):
        value = np.max(self.get_values())
        if not attr:
            self.features.append(["Maximum", value])
        else:
            self.features.append([attr, value])

    # Function to extract variance value from the signal
    # After being extracted values are being saved to the features list.
    def variance(self, attr):
        value = np.var(self.get_values())
        if not attr:
            self.features.append(["Variance", value])
        else:
            self.features.append([attr, value])

    # Function to extract kurtosis value from the signal
    # After being extracted values are being saved to the features list.
    def kurtosis(self, attr):
        value = stat.kurtosis(self.get_values())
        if not attr:
            self.features.append(["Kurtosis", value])
        else:
            self.features.append([attr, value])

    # Function to extract kurtosis value from the signal
    # After being extracted values are being saved to the features list.
    def skewness(self, attr):
        value = stat.skew(self.get_values())
        if not attr:
            self.features.append(["Skewness", value])
        else:
            self.features.append([attr, value])

    # Support function to get values out of a sampled signal
    # Since signal is made out of time stamps and corresponding values
    # sometimes we just want to use the values e.g: feature extraction
    def get_values(self):
        values = list()
        for iterator in range(len(self.signalSamples)):
            values.append(self.signalSamples[iterator][1])

        return values
