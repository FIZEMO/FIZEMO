import csv
import os
import numpy as np
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

    def __init__(self, scenario_name, signal_file_name, signal_type, methods, columns, options=None, windowing_attr=None):
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
            options : dict
                options for scenario (whether save processed signal or draw plot)
            methods : list
                The list of signal's processing methods with their attributes

            """
        self.scenario_name = scenario_name
        self.processing_methods = methods
        self.options = options
        self.processed_signal = Signal(signal_file_name, signal_type, columns, windowing_attr)
        self.processing_info = {}

    def sort_methods_by_order(self):
        """Sorts methods in the scenario by their order"""

        self.processing_methods.sort(key=itemgetter('order'), reverse=False)

    def process_methods(self):
        """Processes all defined methods in the flow scenario"""

        self.sort_methods_by_order()
        for method in self.processing_methods:
            method_to_call = getattr(self.processed_signal, method["functionName"])
            self.processing_info[method["order"]] = method["functionName"]
            if method.get("attributes") is None and method.get("outputLabel") is None:
                method_to_call()
            elif method.get("outputLabel") is None:
                method_to_call(method["attributes"])
            else:
                method_to_call(method["outputLabel"])

    def save_results(self):
        """Writes extracted features and processed signal (if selected) to separate .csv files"""

        date = datetime.now().strftime("%d-%m-%Y %H-%M-%S").__str__()
        features_file_name = self.scenario_name + " " + date
        signal_file_name = self.processed_signal.signal_type + "signal " + features_file_name

        if not os.path.exists("./results/features"):
            os.makedirs("./results/features")
        if not os.path.exists("./results/signals"):
            os.makedirs("./results/signals")

        self.save_feature_csv(features_file_name)

        if self.options is None or "save_processed_signal" not in self.options \
                or self.options["save_processed_signal"].lower() == "true":
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
                self.setup_csv_header(csv_writer)
                csv_writer.writerow([x[0] for x in self.processed_signal.features])
                feature_values = [x[1] for x in self.processed_signal.features]
                feature_values = np.array(feature_values)
                feature_values = feature_values.transpose()
                for row in feature_values:
                    csv_writer.writerow(row)

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

    def setup_csv_header(self, csv_writer):
        header = [str(x) + "=" + str(y) for x, y in self.processing_info.items()]
        scenario_info = "Signal type: " + self.processed_signal.signal_type + " | Windowing: "
        if self.processed_signal.windowing_attributes is None:
            scenario_info += "OFF"
        else:
            scenario_info += "length=" + str(self.processed_signal.windowing_attributes["length"]) + \
                             " slide=" + str(self.processed_signal.windowing_attributes["slide"])

        header = ' '.join(header)
        csv_writer.writerow(["-" * len(header)])
        csv_writer.writerow(["Scenario information: "])
        csv_writer.writerow([scenario_info])
        csv_writer.writerow(["Order of processing methods: "])
        csv_writer.writerow([header])
        csv_writer.writerow(["-" * len(header)])
