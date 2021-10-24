import csv
from datetime import datetime
from signal import Signal
from operator import itemgetter


# Class for a single scenario
#  - scenarioName - name of the scenario taken from JSON configuration file
#  - signalName - name of the file which contains the base signal to be processed
#  - processingMethods - list of methods with attributes and parameters used for signal processing
#                        which are taken from JSON configuration file

class Scenario:

    # Initialization of scenario object
    #   - first argument is name of the scenario
    #   - second argument is name of the file which contains signal data (placed in ./signals)
    #   - third argument is type of signal
    #     (it has to be included in the list of available types of the signal (manual.txt))
    #   - forth argument is list of processing methods
    def __init__(self, scenarioName, signalFileName, signalType, methods):
        self.scenarioName = scenarioName
        self.processingMethods = methods
        self.processedSignal = Signal(signalFileName, signalType)

    # Function for sorting methods in the scenario by their order
    def sort_methods_by_order(self):
        self.processingMethods.sort(key=itemgetter('order'), reverse=False)

    # Function for processing all defined methods in the flow scenario
    def process_methods(self):
        self.sort_methods_by_order()
        for method in self.processingMethods:
            method_to_call = getattr(self.processedSignal, method["function_name"])
            if method.get("attributes") is None and method.get("output_label") is None:
                method_to_call()
            elif method.get("output_label") is None:
                method_to_call(method["attributes"])
            else:
                method_to_call(method["output_label"])

    # Function for writing extracted features to csv file
    def write_csv(self):
        date = datetime.now().strftime("%d-%m-%Y %H-%M-%S").__str__()
        if self.processedSignal.features.__len__() > 0:
            with open("./results/" + self.scenarioName + " " + date + ".csv", 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(['Feature', 'Value'])
                for element in self.processedSignal.features:
                    csvwriter.writerow(element)
