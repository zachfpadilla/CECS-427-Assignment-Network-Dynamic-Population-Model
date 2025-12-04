import matplotlib.pyplot as plt
import networkx as nx

COLOR_MAP = {
    'susceptible': 'blue', 'infected': 'red', 'recovered': 'green',
    'dead': 'black', 'vaccinated': 'cyan', 'sheltered': 'lightgrey', 'active': 'orange'
}

def get_node_colors(G, mode):
    colors = []
    for n in G.nodes():
        attrs = G.nodes[n]
        c = 'grey'
        if mode == 'cascade':
            c = COLOR_MAP['active'] if attrs.get('infected', False) else COLOR_MAP['sheltered']
        else:  # covid mode
            if attrs.get('dead', False):
                c = COLOR_MAP['dead']
            elif attrs.get('infected', False):
                c = COLOR_MAP['infected']
            elif attrs.get('recovered', False):
                c = COLOR_MAP['recovered']
            elif attrs.get('vaccinated', False):
                c = COLOR_MAP['vaccinated']
            elif attrs.get('sheltered', False):
                c = COLOR_MAP['sheltered']
            else:
                c = COLOR_MAP['susceptible']
        colors.append(c)
    return colors

def visualize_step(fig, G, pos, mode, title, anim_delay):
    if not plt.fignum_exists(fig.number): return False
    plt.figure(fig.number)
    plt.clf()
    nx.draw(G, pos, node_color=get_node_colors(G, mode), with_labels=True, node_size=400, font_color='white')
    plt.title(title)
    plt.draw()
    plt.pause(anim_delay)
    return True