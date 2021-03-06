import json
import sys

from scenario import Scenario

""" 
    Defined variables used for distinguishing values obtained from JSON tuple:
    
    SCENARIO_NAME (str) : the name of the scenario
    DICTIONARY ({}) : dictionary with all scenario's parameters
"""

SCENARIO_NAME = 0
DICTIONARY = 1


def load_config_file(path):
    """Loads the JSON configuration file

        Parameters
        ----------
        path : str
            The path to the JSON configuration file

        Returns
        -------
        list of tuples
            a list of tuples, where first parameter is the name of the scenario (SCENARIO_NAME)
            and second parameter is a dictionary with scenario's attributes (DICTIONARY)
        """

    file = open(path)
    config = json.load(file)
    keys = config.keys()
    scenarios = []
    for flow in config:
        # config is a dictionary, where the key is the name of the scenario
        # and value is an array with one element - dictionary with scenario's attributes
        scenarios.append(config[flow][0])

    return list(zip(keys, scenarios))


def convert_json_to_object_list(json_tup_scenarios_list):
    """Converts tuple obtained from loading a json configuration file to list of Scenario objects

        Parameters
        ----------
        json_tup_scenarios_list : []
            The list of tuples, where the first element in each tuple is the scenario name (SCENARIO_NAME)
            and second element is a dictionary with scenario's attributes

        Returns
        -------
        list of scenarios
            a list of Scenario objects filled with data obtained from JSON configuration file
        """

    scenarios = []
    for scenario in json_tup_scenarios_list:
        scenario_object = Scenario(scenario[SCENARIO_NAME],
                                   scenario[DICTIONARY]["signalFileName"],
                                   scenario[DICTIONARY]["signalType"],
                                   scenario[DICTIONARY]["methods"],
                                   scenario[DICTIONARY]["columns_to_read"],
                                   options=scenario[DICTIONARY].get("options", None),
                                   windowing_attr=scenario[DICTIONARY].get("windowing", None))

        scenarios.append(scenario_object)
    return scenarios


def process_scenarios(scenarios):
    """Runs all scenarios

        Parameters
        ----------
        scenarios : []
            The list of Scenario's objects which should be run (all flow scenarios)

        """

    for scenario in scenarios:
        scenario.process_methods()
        scenario.save_results()


def draw_all_signals(scenarios):
    """Test method for plotting all signals obtained from all scenarios

        Parameters
        ----------
        scenarios : []
            The list of Scenario's objects which contain signals to be plotted

        """

    for scenario in scenarios:
        if scenario.options is None or "draw_plot" not in scenario.options \
                or scenario.options["draw_plot"].lower() == "true":
            title = "Processed " + str(scenario.processed_signal.signal_type) + " signal"
            y = str(scenario.processed_signal.signal_type) + " value"
            scenario.processed_signal.draw_plot(scenario.scenario_name, title, 'TimeStamp', y)


#
def main(config_file_path):
    """MAIN SCRIPT

        Scenarios are loaded from .json file as list of tuples, next converted into list of Scenario objects.
        Each Scenario has Signal object which is processed with methods described in the configuration file.
        From each Scenario, which contains feature extraction, there is obtained a result .csv file
        with extracted features and optionally .csv file with processed signal. In the last step there are drawn all the
        processed signals which were chosen by user to print (in configuration file).

    """
    tup_scenarios = load_config_file(config_file_path)
    scenarios = convert_json_to_object_list(tup_scenarios)
    process_scenarios(scenarios)
    draw_all_signals(scenarios)


if __name__ == "__main__":
    main(sys.argv[1])
