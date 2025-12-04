# CECS 427: Market and Strategic Interaction in Network

#### Martin Silva (#030854159), Zachary Padilla (#033497475)

## Dependencies
Required Libraries:
- networkx
- matplotlib

In order to run this project via git:

```
~/: git clone https://github.com/zachfpadilla/CECS-427-Assignment-Network-Dynamic-Population-Model
~/: cd CECS-427-Assignment-Network-Dynamic-Population-Model/

### Optionally ###
~/CECS-427-Assignment-Network-Dynamic-Population-Model/: python3 -m venv .venv
~/CECS-427-Assignment-Network-Dynamic-Population-Model/: source .venv/bin/activate
(.venv) ~/CECS-427-Assignment-Network-Dynamic-Population-Model/: pip install networkx, matplotlib
```

```
(.venv) martin:/home/martin/CECS-427-Assignment-Network-Dynamic-Population-Model -> python3 ./dynamic_population.py -h
usage: dynamic_population.py [-h] [--action {cascade,covid}] [--initiator INITIATOR] [--threshold THRESHOLD] [--probability_of_infection PROBABILITY_OF_INFECTION] [--probability_of_death PROBABILITY_OF_DEATH] [--lifespan LIFESPAN] [--shelter SHELTER]
                             [--vaccination VACCINATION] [--interactive] [--plot]
                             graph_file

Reads the attributes of the nodes and edges in the file. Additional flags allow for additional visualization and more verbose output explaining per-round behavior of bipartite graphs.

positional arguments:
  graph_file            Input file.

options:
  -h, --help            show this help message and exit
  --action {cascade,covid}
                        Either simulates a cascading effect through the network (e.g., information spread) or simulates the spread of a pandemic like COVID-19 across the network.
  --initiator INITIATOR
                        Choose the initial node(s) from which the action will start. (comma-seperated values)
  --threshold THRESHOLD
                        Set the threshold value q (e.g., between 0 and 1) of the cascade effect.
  --probability_of_infection PROBABILITY_OF_INFECTION
                        Set the probability of infection p of the infections
  --probability_of_death PROBABILITY_OF_DEATH
                        Set the probability q of death while infected.
  --lifespan LIFESPAN   Define the lifespan l (e.g., a number of time steps or days) of the rounds.
  --shelter SHELTER     Set the sheltering parameter s (e.g., a proportion or list of nodes that will be sheltered or protected from the infection).
  --vaccination VACCINATION
                        Set the vaccination rate or proportion r (e.g., a number between 0 and 1) representing the proportion of the network that is vaccinated.
  --interactive         Plot the graph and the state of the nodes for every round
  --plot                Plot the number of new infections per day when the simulation completes
```

## Usage Instructions
* ``--plot`` outputs a line plot showing the infections each round/day.
* ``--interactive`` outputs an animated graph showing the node state every round (dead, infected, healthy, sheltered).
* See above flags for more information.
* Cascade only uses `threshold` flag for calculation, COVID requires all other flags (death/infection probabilities, lifespan, sheltered/vaccinated nodes). Default values are provided for each.
* Other intrinsic SIRS attributes are built to take place as well, (recovery rate, immunity loss, etc.)

## Description of Implementation
- All instructions were followed as listed — Interpretations were made where needed.

## Examples of Commands and Outputs
``python ./dynamic_population.py graph.gml --action cascade --initiator 1,2,5 --threshold 0.33 --plot --interactive``
```
Successfully loaded graph from 'graph.gml'.
Nodes: 50, Edges: 236
Starting Cascade with initiators: ['1', '2', '5'], Threshold: 0.33
Cascade finished in 7 rounds.
Total nodes activated: 50
```
![](https://github.com/zachfpadilla/CECS-427-Assignment-Network-Dynamic-Population-Model/blob/main/CASCADE.gif)
![](https://github.com/zachfpadilla/CECS-427-Assignment-Network-Dynamic-Population-Model/blob/main/20251203_23h18m45s_grim.png)

``python ./dynamic_population.py graph.gml --action covid --initiator 3,4 --probability_of_infection 0.5 --shelter 0.1 --vaccination 0.1 --plot --interactive``
```
Successfully loaded graph from 'graph.gml'.
Nodes: 50, Edges: 236
Sheltered nodes: 5
Simulating 10 days...
Simulation completed.
Total infections over 10 days: 42
```
![](https://github.com/zachfpadilla/CECS-427-Assignment-Network-Dynamic-Population-Model/blob/main/COVID.gif)
![](https://github.com/zachfpadilla/CECS-427-Assignment-Network-Dynamic-Population-Model/blob/main/20251203_23h19m17s_grim.png)

