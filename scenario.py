import csv
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
        write_csv()
            Writes extracted features to the csv file.
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
        self.processed_signal = Signal(signal_file_name, signal_type)

    def sort_methods_by_order(self):
        """Sorts methods in the scenario by their order"""

        self.processing_methods.sort(key=itemgetter('order'), reverse=False)

    def process_methods(self):
        """Processes all defined methods in the flow scenario"""

        self.sort_methods_by_order()
        for method in self.processing_methods:
            method_to_call = getattr(self.processed_signal, method["functionName"])
            if method.get("attributes") is None and method.get("outputLabel") is None:
                method_to_call()
            elif method.get("outputLabel") is None:
                method_to_call(method["attributes"])
            else:
                method_to_call(method["outputLabel"])

    def write_csv(self):
        """Writes extracted features to the csv file"""

        date = datetime.now().strftime("%d-%m-%Y %H-%M-%S").__str__()
        if self.processed_signal.features.__len__() > 0:
            with open("./results/" + self.scenario_name + " " + date + ".csv", 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(['Feature', 'Value'])
                for element in self.processed_signal.features:
                    csv_writer.writerow(element)
