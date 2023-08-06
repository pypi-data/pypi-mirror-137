import matplotlib.pyplot as plt
import networkx as nx


def generate_image():
    graph = nx.DiGraph()
    graph.add_nodes_from(['Wood', 'Rock', 'Workers', 'House'])
    graph.add_weighted_edges_from([('Wood', 'Workers', 20), ('Rock', 'Workers', 10), ('Workers', 'House', 15)])
    nx.draw(graph)
    plt.savefig('Graph')
