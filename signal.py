import csv
from datetime import datetime

import peakutils
import scipy.signal as ss
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stat


class Signal:
    """
            A class used to represent a signal

            ...

            Attributes
            ----------
            signal_samples : [[]]
                the two-dimensions list with signal [[timestamps, values]]
            features : [[]]
                the two-dimensions list with extracted features [[name of the feature, value]]
            signal_type : str
                the type of processed signal
                it has to be included in the list of available types of the signal (manual.txt)

            Methods
            -------
            decimate(attr)
                Decimates the signal.
            get_phase_part(attr)
                Gets phase part of given signal.
            z_normalize()
                Normalizes the signal.
            draw_plot(window_name, title_name, x_name, y_name)
                Plots the signal chart with specified names of window, title, x and y values.
            mean(attr)
                Extracts mean value from the signal.
            median(attr)
                Extracts median value from the signal.
            standard_deviation(attr)
                Extracts standard deviation value from the signal.
            minimum(attr)
                Extracts minimum value from the signal.
            maximum(attr)
                Extracts maximum value from the signal.
            variance(attr)
                Extracts variance value from the signal.
            kurtosis(attr)
                Extracts kurtosis value from the signal.
            skewness(attr)
                Extracts skewness value from the signal.
            get_values()
                Support method to get signal values out of a sampled signal.
            """

    def __init__(self, signal_file_name, signal_type, windowing_attr=None):
        """Initialization of the Signal object which include loading the signal from .csv file and
            saving it as signal_samples property

            Parameters
           ----------
           signal_file_name : str
               The name of the file which contains signal data (placed in ./signals)
           signal_type : str
               type of signal
               it has to be included in the list of available types of the signal (manual.txt)

           """

        path = './signals/' + signal_file_name + '.csv'
        pandas_data_framed_signal = pd.read_csv(r'' + path)
        self.signal_type = signal_type
        self.signal_samples = pandas_data_framed_signal.to_numpy()
        self.windowing_attributes = windowing_attr
        self.features = []

    def decimate(self, attr):
        """Decimates the signal

           Parameters
           ----------
           attr : {}
               The dictionary with attributes:
               - "samplingFrequency" is frequency with which signal was sampled
               - "goalFrequency" is goal frequency with which signal should be sampled

           """

        ratio = int(int(attr["samplingFrequency"]) / int(attr["goalFrequency"]))
        self.signal_samples = ss.decimate(self.signal_samples, ratio, 8, axis=0)

    def get_phase_part(self, attr):
        """Gets phase part of given signal

            Parameters
            ----------
            attr : {}
                The dictionary with attributes:
                - "deg" is degree of the polynomial that will estimate the data baseline - default is 10
                - "maxIt" is maximum number of iterations to perform for baseline function - default is 100

            """

        baseline = peakutils.baseline(self.signal_samples[:, 1], deg=attr["deg"], max_it=attr["maxIt"])
        self.signal_samples[:, 1] = [(j-p) for j, p in zip(self.signal_samples[:, 1], baseline)]

    def z_normalize(self):
        """Normalizes the signal."""

        mean = np.mean(self.get_signal_values())
        variance = np.var(self.get_signal_values())

        for i, (timestamps, values) in enumerate(self.signal_samples):
            values = (values - mean) / variance
            self.signal_samples[i][1] = values

    def smooth(self, attr):
        """Removes noise from the signal
            It actually is signal smoothing by averaging the samples.
            For more info visit: https://becominghuman.ai/introduction-to-timeseries-analysis-using-python-numpy-only-3a7c980231af

            Parameters
            ----------
            attr : {}
                The dictionary with attribute:
                - "numberOfIterations" - The number of iterations for the sample smoothing algorithm.

        """

        "We start indexing at 2 because the algorithm needs the previous two samples of the signal to work properly."
        starting_index = 2

        """Signal is an array of two-elements arrays with signal timestamp and value, where value is at the second place.
            In order to get only value we have to point at the index 1 - therefore: value_of_signal = 1
        """
        value_of_signal = 1
        for j in range(int(attr["numberOfIterations"])):
            for i in range(starting_index, len(self.signal_samples)):
                self.signal_samples[i - 1][value_of_signal] = (self.signal_samples[i - 2][value_of_signal] + self.signal_samples[i][value_of_signal]) / 2

    def draw_plot(self, window_name, title_name, x_name, y_name):
        """Plots the signal chart with specified names of window, title, x and y values.

           Parameters
           ----------
           window_name : str
               The name of the chart window
           title_name : str
                The title of the chart
           x_name : str
                The x-axis name
           y_name : str
                The y-axis name
           """

        x_axis, y_axis = zip(*self.signal_samples)
        plt.figure(window_name)
        plt.title(title_name)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.plot(x_axis, y_axis)
        plt.show()

    def mean(self, attr="Mean"):
        """Extracts the mean value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(np.mean(window))

        self.features.append([attr, feature_values])

    def median(self, attr="Median"):
        """Extracts the median value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(np.median(window))

        self.features.append([attr, feature_values])

    def standard_deviation(self, attr="Standard deviation"):
        """Extracts the standard deviation value from the signal. After being extracted,
            values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(np.std(window))

        self.features.append([attr, feature_values])

    def minimum(self, attr="Minimum"):
        """Extracts the minimum value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(np.min(window))

        self.features.append([attr, feature_values])

    def maximum(self, attr="Maximum"):
        """Extracts the maximum value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(np.max(window))

        self.features.append([attr, feature_values])

    def variance(self, attr="Variance"):
        """Extracts the variance value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(np.var(window))

        self.features.append([attr, feature_values])

    def kurtosis(self, attr="Kurtosis"):
        """Extracts the kurtosis value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(stat.kurtosis(window))

        self.features.append([attr, feature_values])

    def skewness(self, attr="Skewness"):
        """Extracts the skewness value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """
        signal_values = self.get_values_for_features()
        feature_values = list()
        for window in signal_values:
            feature_values.append(stat.skew(window))

        self.features.append([attr, feature_values])

    def get_signal_values(self):

        values_list = list()
        for iterator in range(len(self.signal_samples)):
            values_list.append(self.signal_samples[iterator][1])

        return values_list

    def get_values_for_features(self):
        """Support method to get values out of a sampled signal.
            Since signal is made out of time stamps and corresponding values sometimes we just want to use the values
            e.g: feature extraction.

        """

        values = list()

        if self.windowing_attributes is None:
            values.append(self.get_signal_values())
        else:
            values = self.divide_into_windows()

        return values

    def divide_into_windows(self):
        values = list()

        window_start = self.signal_samples[0, 0]
        window_stop = window_start + self.windowing_attributes["length"]

        left_condition = self.signal_samples[:, 0] >= window_start
        right_condition = self.signal_samples[:, 0] <= window_stop

        wind = self.signal_samples[left_condition & right_condition].tolist()
        values.append([x[1] for x in wind])

        while True:
            window_start += self.windowing_attributes["slide"]
            window_stop += self.windowing_attributes["slide"]

            if window_stop > self.signal_samples[-1, 0]:
                break

            left_condition = self.signal_samples[:, 0] >= window_start
            right_condition = self.signal_samples[:, 0] <= window_stop

            wind = self.signal_samples[left_condition & right_condition].tolist()
            values.append([x[1] for x in wind])

        return values
