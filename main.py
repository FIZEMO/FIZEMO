import json
from scenario import Scenario

SCENARIO_NAME = 0
DICTIONARY = 1


# Function for loading a json configuration file
# Returns list of tuples, where first parameter is name of scenario (SCENARIO_NAME),
# second parameter is an array with dictionary (DICTIONARY)
# which contains: name of signal file, type of signal and list of processing methods
# - first argument is path to configuration file
def load_config_file(path):
    file = open(path)
    config = json.load(file)
    keys = config.keys()
    scenarios = []
    for flow in config:
        scenarios.append(config[flow][0])

    return list(zip(keys, scenarios))


# Function for converting tuple obtained from loading a json configuration file to list of Scenario objects
# Returns list of Scenarios filled with data from JSON configuration file
# - first argument is tuple with scenarios data returned from load_config_file()
def convert_json_to_object_list(json_tup_scenarios_list):
    scenarios = []
    for scenario in json_tup_scenarios_list:
        scenario_object = Scenario(scenario[SCENARIO_NAME],
                                   scenario[DICTIONARY]["signalFileName"],
                                   scenario[DICTIONARY]["signalType"],
                                   scenario[DICTIONARY]["methods"])
        scenarios.append(scenario_object)
    return scenarios


# Function for running all scenarios
# - first argument is all flow scenarios (list of Scenario's objects)
def process_scenarios(scenarios):
    for scenario in scenarios:
        scenario.process_methods()
        scenario.write_csv()


# Test function for plotting all signals obtained from all scenarios
# - first argument is a list of Scenarios,
def draw_all_signals(scenarios):
    for scenario in scenarios:
        title = "Processed " + str(scenario.processedSignal.signalType) + " signal"
        x = str(scenario.processedSignal.signalType) + " value"
        scenario.processedSignal.draw_plot(scenario.scenarioName, title, x, 'TimeStamp')


# Scenarios are loaded from .json file as list of tuples, next converted into list of Scenario objects
# Each Scenario has Signal object which is processed with methods described in configuration file
# From each Scenario there is obtained a .csv file with extracted features
def main():
    tup_scenarios = load_config_file("./config.json")
    scenarios = convert_json_to_object_list(tup_scenarios)
    process_scenarios(scenarios)
    draw_all_signals(scenarios)


if __name__ == "__main__":
    main()
