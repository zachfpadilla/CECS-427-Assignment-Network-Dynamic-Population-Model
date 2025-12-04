# CECS 427: Market and Strategic Interaction in Network

#### Martin Silva (#030854159), Zachary Padilla (#033497475)

## Dependencies
Required Libraries:
- networkx
- matplotlib

In order to run this project via git:

```
~/: git clone https://github.com/zachfpadilla/CECS-427-Market-and-Strategic-Interaction-in-Network
~/: cd CECS-427-Market-and-Strategic-Interaction-in-Network/

### Optionally ###
~/CECS-427-Market-and-Strategic-Interaction-in-Network/: python3 -m venv .venv
~/CECS-427-Market-and-Strategic-Interaction-in-Network/: source .venv/bin/activate
(.venv) ~/CECS-427-Market-and-Strategic-Interaction-in-Network/: pip install networkx, matplotlib
```

```
~/CECS-427-Market-and-Strategic-Interaction-in-Network/: python3 ./market_strategy.py -h

usage: market_strategy.py [-h] [--plot] [--interactive]

Python application that performs the market-clearing algorithm with visualizations, as well as optional round graph display.

options:
  --plot                  Plots the output of the command
  --interactive           Plots the output of every round graph (e.g. includes contricted set calculation)
```

## Usage Instructions
* ``--plot`` outputs an image of the plot to a new window.
* ``--interactive`` outputs an image of the round graphs to a new window.

## Description of Implementation
- All instructions were followed as listed—interpretations were made where needed.

## Examples of Commands and Outputs
``python ./market_strategy.py market_constricted.gml --plot``
```
Successfully loaded graph from 'market.gml'.
Nodes: 6, Edges: 9

--- Initial State ---
Seller Prices:
  S3: 0
  S2: 0
  S1: 0

Market cleared; a perfect matching is possible at current prices.
Final Matching (Buyer: Seller):
  B1 -> S1
  B3 -> S2
  B2 -> S3
  S3 -> B2
  S2 -> B3
  S1 -> B1

Generating plot...
Generating plot...
```

<img width="1200" height="759" alt="Screenshot_3" src="https://github.com/user-attachments/assets/e0dd4595-8961-4fc0-b083-0ac22bea0c1c" />

``python ./market_strategy.py market.gml --plot --interactive``
```
Successfully loaded graph from 'market.gml'.
Nodes: 6, Edges: 9

--- Initial State ---
Seller Prices:
  S1: 0
  S3: 0
  S2: 0

----- Round 1 -----
Found constricted set of buyers: {'B1', 'B2'}
Their preferred neighborhood of sellers: {'S1'}
Increasing prices for sellers in the neighborhood...
New Seller Prices:
  S1: 1
  S3: 0
  S2: 0

----- Round 2 -----
Found constricted set of buyers: {'B1', 'B2', 'B3'}
Their preferred neighborhood of sellers: {'S1', 'S2'}
Increasing prices for sellers in the neighborhood...
New Seller Prices:
  S1: 2
  S3: 0
  S2: 1

----- Round 3 -----
Found constricted set of buyers: {'B1', 'B2', 'B3'}
Their preferred neighborhood of sellers: {'S1', 'S2'}
Increasing prices for sellers in the neighborhood...
New Seller Prices:
  S1: 3
  S3: 0
  S2: 2

----- Round 4 -----
Found constricted set of buyers: {'B1', 'B2', 'B3'}
Their preferred neighborhood of sellers: {'S1', 'S2'}
Increasing prices for sellers in the neighborhood...
New Seller Prices:
  S1: 4
  S3: 0
  S2: 3

----- Round 5 -----
Found constricted set of buyers: {'B1', 'B2', 'B3'}
Their preferred neighborhood of sellers: {'S1', 'S2'}
Increasing prices for sellers in the neighborhood...
New Seller Prices:
  S1: 5
  S3: 0
  S2: 4

----- Round 6 -----

Market cleared; a perfect matching is possible at current prices.
Final Matching (Buyer: Seller):
  B1 -> S1
  B2 -> S3
  B3 -> S2
  S1 -> B1
  S3 -> B2
  S2 -> B3

Generating plot...
Generating plot...
```

<img width="1199" height="958" alt="Screenshot_10" src="https://github.com/user-attachments/assets/88624071-ee93-4a96-ba67-090aeab5c4ea" />
