from signal import Signal

import biosppy

from matplotlib import pyplot as plt
import numpy as np
from cmath import sqrt
from statistics import mean, stdev

import pyhrv.nonlinear as nl
import pyhrv.frequency_domain as fd


class PeriodicSignal(Signal):
    """
        Derived class which inherits of the base Signal class.
        It represents the periodic physiological signals and contains variables, features and processing methods
        that are specific only for this type of signal.

        ...

        Attributes
        ----------
        r_peaks_distance: []
            vector with distances between found peaks in milliseconds.
            
        Methods for feature extraction:
        -------
        get_vector_r_peaks_distance_parameters():
            Extract mean, standard deviation, heart rate and RMSSD of distance R vector.
        def get_poincare_parameters():
            Extract SD1 and SD2 values from poincare plot.
        standard_deviation(attr)
            Extracts standard deviation value from the signal.
        def get_psd_parameters(self):
            Extract LF HF, their normalized values and ratio LF/HF.

        Other methods:
        -------
        find_r_peaks(attr)
            Returns R peaks coordinates in seconds.
        calculate_r_peaks_distance(attr)
            Calculate distance between R peaks in seconds.

    """

    def __init__(self, signal_file_name, signal_type, columns, windowing_attr=None):
        super().__init__(signal_file_name, signal_type, columns, windowing_attr)

        self.r_peaks_distance = []

    def pan_tompkins(self, attr):
        """Uses Pan–Tompkins algorithm to extract vector of R-peaks distances.

        In this solution following steps are being executed:
            1) Filter signal with bandpass filter, where user can choose:
                - cut of frequencies: recommended [5, 15]
                - order of the filter
            2) Differentiate the signal.
            3) Square the signal.
            4) Applies moving window integration, where user use can chooose:
                -length of the moving window.
            5) Calculate vector with R-peaks distances


       Parameters
       ----------
       attr : {}
           The dictionary with attributes:
           - samplingRate: int
                rate that the signal has been sampled with
           - filterOrder: int
                order of created butterworth filter
           - cut_of_freq: [int, int]
                an array  of cut of frequencies that will be applied to the filter
           - lengthOfWindow: int
                length of the moving window during moving window integration
        """

        attributes = attr
        attributes["type"] = 'bandpass'

        self.butterworth_filter(attributes)
        self.differentiate()
        self.square()
        self.moving_window_integration(attributes)
        self.calculate_r_peaks_distance(attributes)

    def find_r_peaks(self, attr):
        """Get R peaks coordinates in seconds

           Parameters
           ----------
           attr : {}
               The dictionary with attributes:
               - samplingRate: int
                    rate that the signal has been sampled with
           Returns
           -------
           R peaks coordinates in seconds
               a vector of seconds in which the peak has appeared
        """

        sampling_rate = int(attr["samplingRate"])

        r_peaks = biosppy.signals.ecg.ecg(self.get_values(), sampling_rate=sampling_rate, show=False)
        return r_peaks[2] / sampling_rate

    def calculate_r_peaks_distance(self, attr):
        """Calculate distance between R peaks in seconds."""
        r_peaks = self.find_r_peaks(attr)
        self.r_peaks_distance = [r_peaks[i] - r_peaks[i - 1] for i in np.arange(1, len(r_peaks))]

    def get_vector_r_peaks_distance_parameters(self):
        """Calculate mean, standard deviation, heart rate and RMSSD of distance R vector.
            After being extracted, values are saved to the features list."""
        vector_mean = mean(self.r_peaks_distance)
        vector_sd = stdev(self.r_peaks_distance)
        vector_hr = 60 / vector_mean
        vector_rmsdd = sqrt(sum([pow(vector_mean - x, 2) for x in self.r_peaks_distance]) / (
                self.r_peaks_distance.__len__() - 1)).__abs__()

        self.features.append(["Mean R Distance", np.array([vector_mean])])
        self.features.append(["SD R Distance", np.array([vector_sd])])
        self.features.append(["HR", np.array([vector_hr])])
        self.features.append(["RMSSD", np.array([vector_rmsdd])])

    def get_poincare_parameters(self):
        """Calculate SD1 and SD2 of poincare plot.
            After being extracted, values are saved to the features list."""

        result = nl.poincare(nni=self.r_peaks_distance, show=False)
        plt.close(result["poincare_plot"])

        self.features.append(["SD1", np.array([result['sd1']])])
        self.features.append(["SD2", np.array([result['sd2']])])

    def get_psd_parameters(self):
        """Calculate LF HF, their normalized values and ratio LF/HF.
        After being extracted, values are saved to the features list."""
        result = fd.welch_psd(nni=self.r_peaks_distance, show=False)
        plt.close(result["fft_plot"])

        self.features.append(["LF", np.array([result[2][1]])])
        self.features.append(["HF", np.array([result[2][2]])])
        self.features.append(["LF norm", np.array([result[5][0]])])
        self.features.append(["HF norm", np.array([result[5][1]])])
        self.features.append(["LF/HF", np.array([result[6]])])
