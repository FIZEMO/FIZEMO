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

    def __init__(self, signal_file_name, signal_type):
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

    def z_normalize(self):
        """Normalizes the signal."""

        mean = np.mean(self.get_values())
        variance = np.var(self.get_values())

        for i, (timestamps, values) in enumerate(self.signal_samples):
            values = (values - mean) / variance
            self.signal_samples[i][1] = values

    def noise_filtering(self):
        """Removes noise from the signal
            It actually is signal smoothing by averaging the samples.
            For more info visit: https://becominghuman.ai/introduction-to-timeseries-analysis-using-python-numpy-only-3a7c980231af
        """
        "We start indexing at 2 because the algorithm needs the previous two samples of the signal to work properly."
        starting_index = 2
        for j in range(len(self.signal_samples)):
            for i in range(starting_index, len(self.signal_samples)):
                self.signal_samples[i - 1][1] = (self.signal_samples[i - 2][1] + self.signal_samples[i][1]) / 2

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

        value = np.mean(self.get_values())
        self.features.append([attr, value])

    def median(self, attr="Median"):
        """Extracts the median value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = np.median(self.get_values())
        self.features.append([attr, value])

    def standard_deviation(self, attr="Standard deviation"):
        """Extracts the standard deviation value from the signal. After being extracted,
            values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = np.std(self.get_values())
        self.features.append([attr, value])

    def minimum(self, attr="Minimum"):
        """Extracts the minimum value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = np.min(self.get_values())
        self.features.append([attr, value])

    def maximum(self, attr="Maximum"):
        """Extracts the maximum value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = np.max(self.get_values())
        self.features.append([attr, value])

    def variance(self, attr="Variance"):
        """Extracts the variance value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = np.var(self.get_values())
        self.features.append([attr, value])

    def kurtosis(self, attr="Kurtosis"):
        """Extracts the kurtosis value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = stat.kurtosis(self.get_values())
        self.features.append([attr, value])

    def skewness(self, attr="Skewness"):
        """Extracts the skewness value from the signal. After being extracted, values are saved to the features list.

           Parameters
           ----------
           attr : str
               (optional) The name of the value obtained from "outputLabel" field in JSON configuration file

           """

        value = stat.skew(self.get_values())
        self.features.append([attr, value])

    def get_values(self):
        """Support method to get values out of a sampled signal.
            Since signal is made out of time stamps and corresponding values sometimes we just want to use the values
            e.g: feature extraction.

        """

        values = list()
        for iterator in range(len(self.signal_samples)):
            values.append(self.signal_samples[iterator][1])

        return values
