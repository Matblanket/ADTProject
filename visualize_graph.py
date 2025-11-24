# visualize_algorithms.py
"""
Visualize the coloring of a random k-colorable graph using
FirstFit, CBIP, and FirstFitHeuristic algorithms side by side.
"""

import matplotlib.pyplot as plt
import networkx as nx
from simulation_runner import SimulationRunner
from graph_generator import GraphGenerator

def main():
    # Graph parameters
    n = 25       # number of vertices
    k = 2        # chromatic number
    p = 0.4      # edge probability
    seed = 42    # reproducibility

    # Generate the graph
    gen = GraphGenerator(n, k, p, seed=seed)
    vertices = gen.vertices
    edges = gen.edges
    ordering = gen.get_online_ordering()

    print(f"Generated graph with {n} vertices and {len(edges)} edges.")
    print(f"Online vertex ordering: {ordering}")

    # Create a SimulationRunner instance
    runner = SimulationRunner()

    # List of algorithms to visualize
    algorithms = ['FirstFit', 'CBIP', 'FirstFitHeuristic']
    colorings = {}

    # Color the graph with each algorithm
    for algo in algorithms:
        result = runner.color_single_graph(n, k, p, algo, vertices, edges, ordering)
        colorings[algo] = result['coloring']
        print(f"{algo}: {result['num_colors']} colors used")

    # Build the networkx graph
    G = nx.Graph()
    G.add_nodes_from(vertices)
    G.add_edges_from(edges)

    # Position nodes using spring layout
    pos = nx.spring_layout(G, seed=seed)

    # Plot each algorithm in a subplot
    fig, axes = plt.subplots(1, len(algorithms), figsize=(15, 5))
    for i, algo in enumerate(algorithms):
        ax = axes[i]
        node_colors = [colorings[algo][v] for v in G.nodes()]
        nx.draw(
            G, pos, ax=ax, with_labels=True,
            node_color=node_colors, cmap=plt.cm.tab20, node_size=600,
            edge_color='gray'
        )
        ax.set_title(f"{algo} ({max(node_colors)} colors)")
        ax.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
