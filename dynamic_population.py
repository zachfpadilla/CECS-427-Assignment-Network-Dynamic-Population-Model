import networkx as nx
from cli import get_parser
from visualization import visualize_graph
from interactive_logic import *
from utils import add_attributes
import random
parser = get_parser()
args = parser.parse_args()

G = None

try:
    G = nx.read_gml(args.graph_file)
    print(f"Successfully loaded graph from '{args.graph_file}'.")
    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
except FileNotFoundError:
    print(f"Error: The file '{args.graph_file}' was not found.")
    exit(1)
except Exception as e:
    print(f"Error: Failed to parse GML file. Reason: {e}")
    exit(1)

if not G.is_directed():
    print(f"Error: The GML file does not contain a valid directed graph.")
    exit(1)

add_attributes(G)

mode_arguments = {
        "cascade": [args.threshold],
        "covid": [args.probability_of_infection, args.probability_of_death, args.lifespan, args.shelter, args.vaccination]
        }

# -------------------------
# CASCADE MODE (replacement)
# -------------------------
if args.action == "cascade":
    if any(mode_arguments["covid"]):
        print("Warning: Some arguments will be discarded as they are not used in cascade mode.")

    threshold = args.threshold if args.threshold is not None else 0.5

    if not args.initiator:
        print("Error: Choose an initiator for cascade mode.")
        exit(1)

    # make sure initiator is iterable
    initiators = args.initiator if isinstance(args.initiator, (list, tuple, set)) else [args.initiator]
    for node in initiators:
        G.nodes[node]["infected"] = True

    infections_per_round = []
    new_infection = True
    curr_round = 1

    while new_infection:
        new_infection = False
        to_infect = []
        infection_count = 0

        for node in G.nodes():
            if G.nodes[node].get("infected", False):
                continue

            preds = list(G.predecessors(node))
            if not preds:
                continue

            ratio_infected = sum(1 for n in preds if G.nodes[n].get("infected", False)) / len(preds)
            if ratio_infected >= threshold:
                to_infect.append(node)

        # stage updates so newly infected don't infect in same round
        for node in to_infect:
            G.nodes[node]["infected"] = True
            new_infection = True
            infection_count += 1

        infections_per_round.append(infection_count)

        if args.interactive:
            visualize_graph(G, curr_round)

        curr_round += 1

    if args.plot:
        print("Infections per Round")
        for i, count in enumerate(infections_per_round, start=1):
            print(f"Round {i}: {count}")

# -------------------------
# COVID MODE (replacement)
# -------------------------
elif args.action == "covid":
    if any(mode_arguments["cascade"]):
        print("Warning: Threshold is not used in covid mode. The argument will be discarded.")

    infection_prob = args.probability_of_infection if args.probability_of_infection is not None else 0.5
    death_prob = args.probability_of_death if args.probability_of_death is not None else 0
    lifespan = args.lifespan if args.lifespan is not None else 5
    vaccination_rate = args.vaccination if args.vaccination is not None else 0
    sheltered_nodes = set()

    # sheltered nodes (safe guards)
    if args.shelter:
        if args.shelter["mode"] == "proportion":
            all_nodes = list(G.nodes)
            num_sheltered = min(int(args.shelter["value"] * len(all_nodes)), len(all_nodes))
            if num_sheltered > 0:
                if args.initiator:
                    uninfected_nodes = [node for node in G.nodes if node not in args.initiator]
                sheltered_nodes = set(random.sample(uninfected_nodes, num_sheltered))
            else:
                sheltered_nodes = set()
        elif args.shelter["mode"] == "nodes":
            sheltered_nodes.update(args.shelter["value"])

        for node in sheltered_nodes:
            G.nodes[node]["sheltered"] = True

    # initiators
    if args.initiator:
        initiators = args.initiator if isinstance(args.initiator, (list, tuple, set)) else [args.initiator]
        for node in initiators:
            if node in sheltered_nodes:
                raise Exception("Node cannot be an initiator and sheltered")
            G.nodes[node]["infected"] = True
    else:
        unsheltered_nodes = [n for n in G.nodes if not G.nodes[n].get("sheltered", False)]
        if not unsheltered_nodes:
            raise Exception("No eligible unsheltered nodes to pick an initiator from.")
        G.nodes[random.choice(unsheltered_nodes)]["infected"] = True

    # vaccination (treat vaccination_rate as proportion)
    uninfected_nodes = [n for n in G.nodes if not G.nodes[n].get("infected", False)]
    num_to_vaccinate = min(int(vaccination_rate * len(list(G.nodes))), len(uninfected_nodes))
    if num_to_vaccinate > 0 and uninfected_nodes:
        vaccinated_nodes = set(random.sample(uninfected_nodes, num_to_vaccinate))
    else:
        vaccinated_nodes = set()

    for node in vaccinated_nodes:
        G.nodes[node]["vaccinated"] = True

    # simulation loop with staged infections (no same-round multi-hop)
    infections_per_round = []
    curr_round = 1
    while curr_round <= lifespan:
        newly_infected = []

        # compute currently infectious nodes (skip dead)
        infected_nodes = [n for n in G.nodes if G.nodes[n].get("infected", False) and not G.nodes[n].get("dead", False)]

        for node in infected_nodes:
            # death chance
            if random.random() <= death_prob:
                G.nodes[node]["dead"] = True
                G.nodes[node]["infected"] = False
                continue

            # attempt to infect successors (only susceptibles)
            for succ in G.successors(node):
                if (
                    G.nodes[succ].get("sheltered", False)
                    or G.nodes[succ].get("vaccinated", False)
                    or G.nodes[succ].get("dead", False)
                    or G.nodes[succ].get("infected", False)
                ):
                    continue
                if random.random() <= infection_prob:
                    newly_infected.append(succ)

        # apply staged infections
        for n in newly_infected:
            G.nodes[n]["infected"] = True

        infection_count = len(set(newly_infected))
        infections_per_round.append(infection_count)

        if args.interactive:
            visualize_graph(G, curr_round)

        curr_round += 1

    if args.plot:
        print("Infections per Round")
        for i, count in enumerate(infections_per_round, start=1):
            print(f"Round {i}: {count}")

