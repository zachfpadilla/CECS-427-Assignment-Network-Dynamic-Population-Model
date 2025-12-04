import sys

def resolve_initiators(G, arg_initiator):
    if isinstance(arg_initiator, str):
        candidates = [x.strip() for x in arg_initiator.split(',')]
    elif isinstance(arg_initiator, (list, tuple, set)):
        candidates = arg_initiator
    else:
        candidates = [arg_initiator]

    valid_nodes = []
    graph_nodes = set(G.nodes())
    for c in candidates:
        if c in graph_nodes:
            valid_nodes.append(c)
        elif str(c).isdigit() and int(c) in graph_nodes:  # try casting to int
            valid_nodes.append(int(c))

    if not valid_nodes:
        print(f"Error: None of the initiators {candidates} were found in the graph.")
        sys.exit(1)
    return valid_nodes