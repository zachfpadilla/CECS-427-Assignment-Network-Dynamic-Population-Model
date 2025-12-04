import networkx as nx
import matplotlib.pyplot as plt
from cli import get_parser
from utils import add_attributes
from visualization import visualize_step
from misc_handling import resolve_initiators
import random
import sys


parser = get_parser()
args = parser.parse_args()
G = None

RECOVERY_PROB = 0.2
IMMUNITY_LOSS_PROB = 0.05
ANIMATION_DELAY = 0.5


# ran into an issue with infinite windows after closing main simulation
simulation_running = True


def handle_close(event):
    global simulation_running
    print("\nSimulation window closed. Stopping...")
    simulation_running = False


# moved previously-implemented code to bottom
try:
    G = nx.read_gml(args.graph_file)
    print(f"Successfully loaded graph from '{args.graph_file}'.")
    print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}")
except Exception as e:
    print(f"Error loading graph: {e}")
    sys.exit(1)

if not G.is_directed():
    print(f"Error: The GML file does not contain a valid directed graph.")
    sys.exit(1)

add_attributes(G)
pos = nx.spring_layout(G, seed=42)

# setup interactive plot
fig = None
if args.interactive:
    fig = plt.figure(figsize=(10, 8))
    fig.canvas.mpl_connect('close_event', handle_close)
    plt.ion()

mode_arguments = {
    "cascade": [args.threshold],
    "covid": [args.probability_of_infection, args.probability_of_death, args.lifespan, args.shelter,
              args.vaccination]
}

# safe argument parsing
initiators = []
if args.initiator:
    initiators = resolve_initiators(G, args.initiator)

# -------------------------
# CASCADE MODE (replacement)
# -------------------------
if args.action == "cascade":
    if any(mode_arguments["covid"]):
        print("Warning: Covid arguments ignored in cascade mode.")

    threshold = float(args.threshold) if args.threshold is not None else 0.5

    if not initiators:
        print("Error: Choose an initiator for cascade mode.")
        sys.exit(1)

    print(f"Starting Cascade with initiators: {initiators}, Threshold: {threshold}")

    for node in initiators:
        G.nodes[node]["infected"] = True

    # track day 0 so plot isn't empty
    infections_per_round = [len(initiators)]

    if args.interactive and simulation_running:
        visualize_step(fig, G, pos, 'cascade', "Cascade: Start", ANIMATION_DELAY)

    new_infection = True
    curr_round = 1

    while new_infection and simulation_running:
        new_infection = False
        to_infect = []

        for node in G.nodes():
            if G.nodes[node].get("infected", False): continue
            preds = list(G.predecessors(node))
            if not preds: continue

            ratio_infected = sum(1 for n in preds if G.nodes[n].get("infected", False)) / len(preds)
            if ratio_infected >= threshold: to_infect.append(node)

        for node in to_infect:
            G.nodes[node]["infected"] = True
            new_infection = True

        infections_per_round.append(len(to_infect))

        if args.interactive:
            if not simulation_running: break
            visualize_step(fig, G, pos, 'cascade', f"Cascade: Round {curr_round}", ANIMATION_DELAY)
        curr_round += 1

    if simulation_running:
        print(f"Cascade finished in {curr_round - 1} rounds.")
        print(f"Total nodes activated: {sum(infections_per_round)}")

    if args.plot and simulation_running:
        if args.interactive: plt.ioff()
        plt.figure(figsize=(10, 6))
        # start x-axis at 0 to show initiators
        plt.plot(range(0, len(infections_per_round)), infections_per_round, marker='o', linestyle='-',
                 color='orange')
        plt.title("Cascade: New Activations per Round")
        plt.xlabel("Round")
        plt.ylabel("New Activations")
        plt.grid(True)
        plt.show()

# -------------------------
# COVID MODE (replacement)
# -------------------------
elif args.action == "covid":
    if any(mode_arguments["cascade"]):
        print("Warning: Threshold argument ignored in covid mode.")

    infection_prob = float(args.probability_of_infection) if args.probability_of_infection is not None else 0.5
    death_prob = float(args.probability_of_death) if args.probability_of_death is not None else 0.0
    lifespan = int(args.lifespan) if args.lifespan is not None else 10

    # robust shelter parsing
    sheltered_nodes = set()
    if args.shelter:
        if isinstance(args.shelter, dict):
            if args.shelter["mode"] == "proportion":
                num_sheltered = int(args.shelter["value"] * len(G.nodes))
                candidates = [n for n in G.nodes if n not in initiators]
                if candidates: sheltered_nodes.update(
                    random.sample(candidates, min(len(candidates), num_sheltered)))
            elif args.shelter["mode"] == "nodes":
                sheltered_nodes.update(args.shelter["value"])
        else:  # fallback for float
            num_sheltered = int(float(args.shelter) * len(G.nodes))
            candidates = [n for n in G.nodes if n not in initiators]
            if candidates: sheltered_nodes.update(random.sample(candidates, min(len(candidates), num_sheltered)))

    for node in sheltered_nodes: G.nodes[node]["sheltered"] = True
    print(f"Sheltered nodes: {len(sheltered_nodes)}")

    # initiator setup (using parsed initiators)
    valid_initiators = []
    if initiators:
        for n in initiators:
            if n in sheltered_nodes:
                print(f"Warning: Initiator {n} is sheltered. Skipping.")
                continue
            G.nodes[n]["infected"] = True
            valid_initiators.append(n)
    else:
        unsheltered = [n for n in G.nodes if not G.nodes[n].get("sheltered", False)]
        if unsheltered:
            start_node = random.choice(unsheltered)
            G.nodes[start_node]["infected"] = True
            valid_initiators.append(start_node)

    # vaccination setup
    vaccination_rate = float(args.vaccination) if args.vaccination is not None else 0.0
    uninfected = [n for n in G.nodes if not G.nodes[n].get("infected", False)]
    num_vax = int(vaccination_rate * len(G.nodes))
    if num_vax > 0 and uninfected:
        for node in random.sample(uninfected, min(len(uninfected), num_vax)):
            G.nodes[node]["vaccinated"] = True

    # track day 0
    infections_per_round = [len(valid_initiators)]

    if args.interactive and simulation_running:
        visualize_step(fig, G, pos, 'covid', "COVID: Day 0", ANIMATION_DELAY)

    curr_round = 1
    print(f"Simulating {lifespan} days...")

    while curr_round <= lifespan and simulation_running:
        newly_infected = []
        newly_recovered = []
        newly_dead = []
        newly_susceptible = []

        # immunity loss
        for n in [x for x in G.nodes if G.nodes[x].get("recovered", False)]:
            if random.random() <= IMMUNITY_LOSS_PROB:
                newly_susceptible.append(n)

        # spread (first), then death/recovery
        infected = [n for n in G.nodes if G.nodes[n].get("infected", False) and not G.nodes[n].get("dead", False)]
        for node in infected:
            # spread
            for succ in G.successors(node):
                if (G.nodes[succ].get("sheltered", False) or G.nodes[succ].get("vaccinated", False) or
                        G.nodes[succ].get("dead", False) or G.nodes[succ].get("recovered", False) or G.nodes[
                            succ].get("infected", False)):
                    continue
                if random.random() <= infection_prob:
                    newly_infected.append(succ)

            # status check
            if random.random() <= death_prob:
                newly_dead.append(node)
            elif random.random() <= RECOVERY_PROB:
                newly_recovered.append(node)

        # apply updates
        for n in newly_dead: G.nodes[n].update({"infected": False, "dead": True})
        for n in newly_recovered: G.nodes[n].update({"infected": False, "recovered": True})
        for n in newly_susceptible: G.nodes[n]["recovered"] = False
        for n in set(newly_infected): G.nodes[n]["infected"] = True

        infections_per_round.append(len(set(newly_infected)))

        if args.interactive:
            if not simulation_running: break
            visualize_step(fig, G, pos, 'covid', f"COVID: Day {curr_round}", ANIMATION_DELAY)
        curr_round += 1

    if simulation_running:
        print("Simulation completed.")
        print(f"Total infections over {lifespan} days: {sum(infections_per_round)}")

    if args.plot and simulation_running:
        if args.interactive: plt.ioff()
        plt.figure(figsize=(10, 6))
        # plot from 0 to lifespan
        plt.plot(range(0, len(infections_per_round)), infections_per_round, marker='o', linestyle='-', color='red')
        plt.title("COVID (SIRS): New Infections per Day")
        plt.xlabel("Day")
        plt.ylabel("New Infections")
        plt.grid(True)
        plt.show()