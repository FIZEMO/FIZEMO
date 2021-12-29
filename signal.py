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
            windowing_attributes : dict
                Dictionary which contains information about the windowing, like: length of the window and its slide.
                If set to None - there is no windowing included.



            Methods for signal processing:
            -------
            butterworth_filter(attr)
                Creates and applies filter on the signal.
            differentiate()
                Differentiate the signal.
            square()
                Squares values of the signal.
            moving_window_integration(attr)
                Integrates the signal with moving window function.
            decimate(attr)
                Decimates the signal.
            get_phase_part(attr)
                Gets phase part of given signal.
            z_normalize()
                Normalizes the signal.
            smooth()
                Smooths the signal by averaging the samples.


            Methods for feature extraction:
            Additional information for programmers:
            In all methods for feature extraction there is implemented a mechanism of extraction for windowed signal.
            To add new method for feature extraction one need to:
                I. Name the method in understandable way (the same name will be used in configuration file)
                II. Set default attrubute name (for .csv) in passed parameter
                III. Get windowed signal values with method "get_windowed_values()"
                IV. Calculate feature for each window in the loop and save results in array
            -------
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


            Other methods:
            -------
            draw_plot(window_name, title_name, x_name, y_name)
                Plots the signal chart with specified names of window, title, x and y values.
            get_values()
                Support method to get signal values out of a sampled signal.
            get_windowed_values()
                Method to get values out of a sampled signal and decide whether returned signal should be windowed or not.
            get_window_timestamps()
                Support method to get timestamps out of a sampled signal and divide them into windows timestamps.
            divide_into_windows():
                Support method to get values out of a sampled signal and divide them into windows
            set_values(new_values)
                Support method for setting new for the signal.
            """

    def __init__(self, signal_file_name, signal_type, columns, windowing_attr=None):
        """Initialization of the Signal object which include loading the signal from .csv file and
            saving it as signal_samples property

            Parameters
           ----------
           signal_file_name : str
               The name of the file which contains signal data (placed in ./signals)
           signal_type : str
               type of signal
               it has to be included in the list of available types of the signal (manual.txt)
           columns : dict
               Dictionary which contains information about columns to read from .csv file with signal data
                with specified: "timestamp" column number and "values" column number (values for the signal)
           windowing_attr : dict
                Dictionary which contains information about the windowing, like: length of the window and its slide.
                If set to None - there is no windowing included.

           """

        path = './signals/' + signal_file_name + '.csv'
        pandas_data_framed_signal = pd.read_csv(r'' + path)
        columns_names = pandas_data_framed_signal.columns
        columns_selected = list()
        columns_selected.append(columns_names[columns["timestamp"]-1])
        columns_selected.append(columns_names[columns["values"]-1])

        pandas_data_framed_signal = pandas_data_framed_signal[columns_selected]
        self.signal_type = signal_type
        self.signal_samples = pandas_data_framed_signal.to_numpy()
        self.windowing_attributes = windowing_attr
        self.features = []

    def butterworth_filter(self, attr):
        """Creating and using Butterworth digital filter

           Parameters
           ----------
           attr : {}
               The dictionary with attributes:
               - samplingRate: int
                    rate that the signal has been sampled with
               - filterOrder: int
                    order of created filter
               - type: str
                    type of created filter. Available types:
                        'lowpass',
                        'highpass'
                        'bandpass'
                        'bandstop'
               - cut_of_freq: int | [int, int]
                    an array or a scalar of cut of frequencies that will be aplied to the filter
                        Scalar for 'lowpass' and 'highpass' filter.
                        Array for 'bandpass' and 'bandstop' filter.
           """

        order = attr["filterOrder"]
        freq = attr["samplingRate"]
        type = attr["type"]
        cut_of_freq = attr["cutOfFrequencies"]

        nyquist_freq = 0.5 * freq

        """Normalization of frequency values by the Nyquist frequency f = f / fn"""
        if isinstance(cut_of_freq, list):
            cut_of_freq = [elem / nyquist_freq for elem in cut_of_freq]
        else:
            cut_of_freq = cut_of_freq / nyquist_freq

        """Creating coefficients of the filter"""
        b, a = ss.butter(order, cut_of_freq, btype=type, analog=False)

        """Applying created filter's coefficients to the signal.Filtered signal is applied only to the values of the signal. 
             It did not changed the timestamps."""
        filtered_values = ss.lfilter(b, a, self.get_values())
        self.set_values(filtered_values)

    def differentiate(self):
        """Differentiate the signal"""

        differentiated_signal = np.ediff1d(self.get_values())
        self.set_values(differentiated_signal)

    def square(self):
        """Squares the signal"""

        squared_signal = np.square(self.get_values())
        self.set_values(squared_signal)

    def moving_window_integration(self, attr):
        """Integrate the signal with moving frame of the given length

           Parameters
           ----------
           attr : {}
               The dictionary with attributes:
               - lengthOfWindow: int
                    length of the moving window
           """

        length_of_window = attr["lengthOfWindow"]

        integrated_signal = np.convolve(self.get_values(), np.ones(length_of_window))
        self.set_values(integrated_signal)

    def decimate(self, attr):
        """Decimates the signal

           Parameters
           ----------
           attr : {}
               The dictionary with attributes:
               - samplingFrequency: int
                    frequency with which signal was sampled
               - goalFrequency: int
                    goal frequency with which signal should be sampled
           """
        sampling_frequency = int(attr["samplingFrequency"])
        goal_frequency = int(attr["goalFrequency"])

        ratio = int(sampling_frequency / goal_frequency)
        self.signal_samples = ss.decimate(self.signal_samples, ratio, 8, axis=0)

    def get_phase_part(self, attr):
        """Gets phase part of given signal

            Parameters
            ----------
            attr : {}
                The dictionary with attributes:
                - deg: int
                    degree of the polynomial that will estimate the data baseline - recommended is 10
                - maxIt: int
                    maximum number of iterations to perform for baseline function - recommended is 100
            """
        degree = attr["deg"]
        max_iterations = attr["maxIt"]

        baseline = peakutils.baseline(self.signal_samples[:, 1], deg=degree, max_it=max_iterations)
        self.signal_samples[:, 1] = [(j - p) for j, p in zip(self.signal_samples[:, 1], baseline)]

    def z_normalize(self):
        """Normalizes the signal."""

        mean = np.mean(self.get_values())
        variance = np.var(self.get_values())

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
                - numberOfIterations: int
                    The number of iterations for the sample smoothing algorithm.
        """

        "We start indexing at 2 because the algorithm needs the previous two samples of the signal to work properly."
        starting_index = 2

        """Signal is an array of two-elements arrays with signal timestamp and value, where value is at the second place.
            In order to get only value we have to point at the index 1 - therefore: value_of_signal = 1
        """
        value_of_signal = 1
        for j in range(int(attr["numberOfIterations"])):
            for i in range(starting_index, len(self.signal_samples)):
                self.signal_samples[i - 1][value_of_signal] = (self.signal_samples[i - 2][value_of_signal] +
                                                               self.signal_samples[i][value_of_signal]) / 2

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

        signal_values = self.get_windowed_values()
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

        signal_values = self.get_windowed_values()
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

        signal_values = self.get_windowed_values()
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

        signal_values = self.get_windowed_values()
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

        signal_values = self.get_windowed_values()
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

        signal_values = self.get_windowed_values()
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

        signal_values = self.get_windowed_values()
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
        signal_values = self.get_windowed_values()
        feature_values = list()
        for window in signal_values:
            feature_values.append(stat.skew(window))

        self.features.append([attr, feature_values])

    def get_values(self):
        """Support method to get values out of a sampled signal.
                    Since signal is made out of time stamps and corresponding values sometimes we just want to use the values
                    e.g: feature extraction.

                """

        values_list = list()
        for iterator in range(len(self.signal_samples)):
            values_list.append(self.signal_samples[iterator][1])

        return values_list

    def get_windowed_values(self):
        """Method to get values out of a sampled signal and decide whether returned signal should be windowed or not.
         Method returns a 2 dimensional array where each element represents a window with signal values if it is windowed
         or it has only one element with whole signal if it is not windowed.
                       """
        values = list()

        if self.windowing_attributes is None:
            values.append(self.get_values())
        else:
            values = self.divide_into_windows()

        return values

    def get_window_timestamps(self):
        """Support method to get timestamps out of a sampled signal and divide them into windows timestamps.
                                       """
        timestamps = list()

        window_start = self.signal_samples[0, 0]
        window_stop = window_start + self.windowing_attributes["length"]
        timestamps.append([window_start, window_stop])

        while True:
            window_start += self.windowing_attributes["slide"]
            window_stop += self.windowing_attributes["slide"]
            if window_stop > self.signal_samples[-1, 0]:
                break
            timestamps.append([window_start, window_stop])

        if len(self.features) == 0:
            start_timestamps = [x[0] for x in timestamps]
            self.features.append(["Start Window Timestamp", start_timestamps])

        return timestamps

    def divide_into_windows(self):
        """Support method to get values out of a sampled signal and divide them into windows with attributes -
                    length of window and slide - selected by user in configuration file. Method returns a 2 dimensional array where each element
                        represents a window with signal values.
                               """

        values = list()
        timestamps = self.get_window_timestamps()

        for window in timestamps:
            window_start = window[0]
            window_stop = window[1]

            left_condition = self.signal_samples[:, 0] >= window_start
            right_condition = self.signal_samples[:, 0] <= window_stop

            wind = self.signal_samples[left_condition & right_condition].tolist()
            values.append([x[1] for x in wind])

        return values

    def set_values(self, new_values):
        """Support method for setting new for the signal.
            Since signal is made out of time stamps and corresponding values sometimes we just want to set new values
        """

        length_of_values = len(self.signal_samples)
        length_of_new_values = len(new_values)

        if length_of_values > length_of_new_values:
            length_of_vector = length_of_new_values
        else:
            length_of_vector = length_of_values

        for index in range(length_of_vector):
            self.signal_samples[index][1] = new_values[index]
