import json
import numpy as np
from operator import itemgetter
import classes


# Function for loading a json configuration file
# Returns list of tuples, where first parameter is name of scenario, second parameter is list of methods
# - first argument is path to configuration file

def load_config_file(path):
    file = open(path)
    config = json.load(file)
    keys = config.keys()
    scenarios = []
    for flow in config:
        scenarios.append(config[flow])

    return list(zip(keys, scenarios))


# Function for sorting methods in all scenarios by their order
# - first argument is list of flows with methods
def sort_methods_by_order(flow_scenarios):
    for scenario in flow_scenarios:
        scenario.sort(key=itemgetter('order'), reverse=False)


# Returns the list of numbers, which indicates on which position next scenarios differes
# For example if scenario 1 and scenario 2 have two the same processing methods at the beggining of flow
# and then they differs, and scenario 2 and scenario 3 have three the same processing methods at the beggining of flow
# and then they differs, it returns list: [2, 3]
# If whole processing for two scenarios are the same it returns -1

def compare_scenarios(flow_scenarios):
    list_of_differ_positions = []

    for i in range(len(flow_scenarios) - 1):
        scenario_a = np.array(flow_scenarios[i])
        scenario_b = np.array(flow_scenarios[i + 1])

        if len(scenario_a) > len(scenario_b):
            scenario_b.resize((1, len(scenario_a)))
            scenario_b = np.squeeze(scenario_b)
        elif len(scenario_a) < len(scenario_b):
            scenario_a = scenario_a.resize((1, len(scenario_b)))
            scenario_a = np.squeeze(scenario_a)

        for (function_a, function_b) in zip(scenario_a, scenario_b):
            if function_a != 0 and function_b != 0:
                if function_a["function_name"] != function_b["function_name"] or function_a["attributes"] != function_b[
                    "attributes"]:
                    differ_num = function_a["order"]
                    break
            else:
                if function_a != 0:
                    differ_num = function_a["order"]
                else:
                    differ_num = function_b["order"]
                break

            differ_num = -1

        list_of_differ_positions.append(differ_num)

    return list_of_differ_positions


# Function for processing all methods in one flow scenario
# - first argument is flow scenario (not tuple, only methods)
# - second argument is signal which should be processed
def run_methods_from_scenario(flow_scenario, signal):
    for method in flow_scenario:
        fun = getattr(signal, method["function_name"])
        fun(method["attributes"])


# Function for running all scenarios on created signals from file
# - first argument is all flow scenarios
# (list of tuples, where first value is name of flow and second value is list of methods to run)
# - second argument is name of .csv file placed in /signals dictionary
def process_scenarios(tup_scenarios, signalFileName):
    signals = {}
    for scenario in tup_scenarios:
        signal = classes.Signal(signalFileName)
        run_methods_from_scenario(scenario[1], signal)
        signals[scenario[0]] = signal
    return signals


# Test function for drawing all signals from signals dictionary
# - first argument is a dictionary with signals,
# where the key is name of flow and value is the signal received from its flow
def draw_all_signals(signals):
    for (signal, flow_name) in list(zip(signals.values(), signals.keys())):
        signal.draw_plot(flow_name, 'Decimated GSR signal', 'GSR value', 'TimeStamp')


# Signals are stored in a dictionary, where  key is a name of flow and value is a received signal from processing flow
# Scenarios are loaded from .json file as list of tuples
# where first element of tuple is name of flow and second element is list of preprocessing methods
def main():
    tup_scenarios = load_config_file("./config.json")
    sort_methods_by_order([x[1] for x in tup_scenarios])
    differ_positions = compare_scenarios([x[1] for x in tup_scenarios])
    print("Next scenarios differ in positions: ")
    print(differ_positions)
    signals = process_scenarios(tup_scenarios, 'rawGSR')
    print([x.signalSamples for x in signals.values()])
    draw_all_signals(signals)
    print("First scenario:", signals["flow_1"].features)


if __name__ == "__main__":
    main()
