import csv
import os
from datetime import datetime
from signal import Signal
from operator import itemgetter


class Scenario:
    """
        A class used to represent a single scenario

        ...

        Attributes
        ----------
        scenario_name : str
            the name of the scenario taken from JSON configuration file
        processed_signal : Signal
            the object of Signal to be processed
        processing_methods : list
            list of methods with attributes and parameters used for signal processing
            which are taken from JSON configuration file
        windowing_mode : boolean
            flag which sets true when windowing starts
        windowing_info : dict
            dictionary which contains all information about windowing
        write_to_csv : [[]]
            array with extended elements: first element contains headers for csv, rest contains values for each row

        Methods
        -------
        sort_methods_by_order()
            Sorts methods in the scenario by their order.
        process_methods()
            Processes the signal with all methods defined in the flow scenario.
        save_results()
            Writes extracted features and processed signal to separate .csv files
        save_feature_csv()
            Writes extracted features to the csv file and call function to write the processed signal to csv file.
        save_signal_csv()
            Writes processed signal to the csv file.
        """

    def __init__(self, scenario_name, signal_file_name, signal_type, methods):
        """Initialization of the Scenario object

            Parameters
            ----------
            scenario_name : str
                The name of the scenario
            signal_file_name : str
                The name of the file which contains signal data (placed in ./signals)
            signal_type : str
                type of signal
                it has to be included in the list of available types of the signal (manual.txt)
            methods : list
                The list of signal's processing methods with their attributes

            """
        self.scenario_name = scenario_name
        self.processing_methods = methods
        self.windowing_mode = False
        self.windowing_info = {}
        self.processed_signal = Signal(signal_file_name, signal_type)
        self.write_to_csv = []

    def sort_methods_by_order(self):
        """Sorts methods in the scenario by their order"""

        self.processing_methods.sort(key=itemgetter('order'), reverse=False)

    def process_methods(self):
        """Processes all defined methods in the flow scenario"""

        self.sort_methods_by_order()

        for method in self.processing_methods:
            if method["functionName"] != "windowing":
                method_to_call = getattr(self.processed_signal, method["functionName"])
                if method.get("attributes") is None and method.get("outputLabel") is None:
                    method_to_call()
                elif method.get("outputLabel") is None:
                    method_to_call(method["attributes"])
                else:
                    method_to_call(method["outputLabel"])
            else:
                self.windowing_mode = True
                self.windowing_info.update(method)
                self.processed_signal.main_signal = self.processed_signal.signal_samples
                break

        if self.windowing_mode:
            window_start = self.processed_signal.main_signal[0, 0]
            window_stop = window_start + self.windowing_info["attributes"]["length"]

            left_condition = self.processed_signal.main_signal[:, 0] >= window_start
            right_condition = self.processed_signal.main_signal[:, 0] <= window_stop

            self.processed_signal.signal_samples = self.processed_signal.main_signal[left_condition & right_condition]
            self.write_to_csv.clear()
            self.processed_signal.features.clear()

            while True:
                if self.write_to_csv:
                    window_start += self.windowing_info["attributes"]["slide"]
                    window_stop += self.windowing_info["attributes"]["slide"]

                    left_condition = self.processed_signal.main_signal[:, 0] >= window_start
                    right_condition = self.processed_signal.main_signal[:, 0] <= window_stop

                    self.processed_signal.signal_samples = self.processed_signal.main_signal[left_condition & right_condition]

                for index in range(self.windowing_info["order"], self.processing_methods.__len__()):
                    method = self.processing_methods[index]
                    method_to_call = getattr(self.processed_signal, method["functionName"])
                    if method.get("attributes") is None and method.get("outputLabel") is None:
                        method_to_call()
                    elif method.get("outputLabel") is None:
                        method_to_call(method["attributes"])
                    else:
                        method_to_call(method["outputLabel"])

                if not self.write_to_csv:
                    self.write_to_csv.append([x[0] for x in self.processed_signal.features])
                    self.write_to_csv.append([x[1] for x in self.processed_signal.features])
                else:
                    self.write_to_csv.append([x[1] for x in self.processed_signal.features])

                self.processed_signal.features.clear()

                if window_stop > self.processed_signal.main_signal[-1, 0]:
                    break

        elif self.processed_signal.features:
            self.processed_signal.main_signal = self.processed_signal.signal_samples
            self.write_to_csv.append([x[0] for x in self.processed_signal.features])
            self.write_to_csv.append([x[1] for x in self.processed_signal.features])
        else:
            self.processed_signal.main_signal = self.processed_signal.signal_samples

    def save_results(self):
        """Writes extracted features and processed signal to separate .csv files"""

        date = datetime.now().strftime("%d-%m-%Y %H-%M-%S").__str__()
        features_file_name = self.scenario_name + " " + date
        signal_file_name = self.processed_signal.signal_type + "signal " + features_file_name

        if not os.path.exists("./results/features"):
            os.makedirs("./results/features")
        if not os.path.exists("./results/signals"):
            os.makedirs("./results/signals")

        self.save_feature_csv(features_file_name)
        self.save_signal_csv(signal_file_name)

    def save_feature_csv(self, file_name):
        """Writes extracted features to the csv file and call function to write the processed signal to csv file

            Parameters
           ----------
           file_name : str
               The name of the newly created file which contains extracted features data
               (will be placed in ./results/features/).
               The name is compatible with the signal file name which is also saved after running the scenario.
        """

        if self.processed_signal.features.__len__() > 0:
            with open("./results/features/" + file_name + ".csv", 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)

                if self.windowing_mode:
                    csv_writer.writerow(["Window length: "+str(self.windowing_info["attributes"]["length"])+" ms"])
                csv_writer.writerows(self.write_to_csv)

    def save_signal_csv(self, file_name):
        """Writes processed signal to the csv file

           Parameters
           ----------
           file_name : str
               The name of the newly created file which contains processed signal data
               (will be placed in ./results/signals/).
               The name bases on the scenario file name which was used to process the signal.
        """

        with open("./results/signals/" + file_name + ".csv", 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for element in self.processed_signal.signal_samples:
                csv_writer.writerow(element)
