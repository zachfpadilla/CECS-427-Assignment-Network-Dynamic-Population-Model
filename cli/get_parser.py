import argparse

def comma_separated_list(value):
    items = value.split(",")
    if not items or any(not item.strip() for item in items):
        raise argparse.ArgumentTypeError("Values must be comma-separated")
    return items

def normalized_value(value):
    try:
        num = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError("Value must be a valid number.")

    if num < 0 or num > 1:
        raise argparse.ArgumentTypeError("Value must be between 0 and 1.")
    return num

def shelter_value(value):
    # Try proportion first
    try:
        return {
            "mode": "proportion",
            "value": normalized_value(value)
        }
    except argparse.ArgumentTypeError:
        pass

    # Try comma-separated node list
    try:
        return {
            "mode": "nodes",
            "value": comma_separated_list(value)
        }
    except argparse.ArgumentTypeError:
        pass

    # If both fail
    raise argparse.ArgumentTypeError(
        "Shelter must be either a float between 0 and 1 "
        "or a comma-separated list of nodes"
    )

def get_parser():
    """ Returns a custom argparse parser made for graph.py """
    parser = argparse.ArgumentParser(description='Reads the attributes of the nodes and edges in the file. Additional flags allow for additional visualization and more verbose output explaining per-round behavior of bipartite graphs.', formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument("graph_file", help="Input file.")
    parser.add_argument("--action", choices=["cascade", "covid"], help="Either simulates a cascading effect through the network (e.g., information spread) or simulates the spread of a pandemic like COVID-19 across the network.")

    parser.add_argument("--initiator", type=comma_separated_list, help="Choose the initial node(s) from which the action will start. (comma-seperated values)")
    
    parser.add_argument("--threshold", type=normalized_value, help="Set the threshold value q (e.g., between 0 and 1) of the cascade effect.")

    parser.add_argument("--probability_of_infection", type=normalized_value, help="Set the probability of infection p of the infections")
    parser.add_argument("--probability_of_death", type=normalized_value, help="Set the probability q of death while infected.")
    parser.add_argument("--lifespan", type=int, help="Define the lifespan l (e.g., a number of time steps or days) of the rounds.")
    parser.add_argument("--shelter", type=shelter_value, help="Set the sheltering parameter s (e.g., a proportion or list of nodes that will be sheltered or protected from the infection).")
    parser.add_argument("--vaccination", type=normalized_value, help="Set the vaccination rate or proportion r (e.g., a number between 0 and 1) representing the proportion of the network that is vaccinated.")

    parser.add_argument("--interactive", action="store_true", help="Plot the graph and the state of the nodes for every round")
    parser.add_argument("--plot", action="store_true", help="Plot the number of new infections per day when the simulation completes")

    return parser
