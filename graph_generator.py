"""
Random Online k-colourable Graph Generator

This module generates random k-colourable graphs following the pseudocode
from the project specification. Graphs are stored in EDGES format.
"""

import random
import os
from typing import List, Tuple, Set


class GraphGenerator:
    """Generates random k-colourable online graphs."""
    
    def __init__(self, n: int, k: int, p: float, seed: int = None):
        """
        Initialize graph generator.
        
        Args:
            n: Number of vertices
            k: Number of independent sets (chromatic number)
            p: Probability of adding an edge between vertices in different sets
            seed: Random seed for reproducibility
        """
        self.n = n
        self.k = k
        self.p = p
        if seed is not None:
            random.seed(seed)
        from kcol_graph_gen import KColorableGraphGenerator
        generator = KColorableGraphGenerator(seed=42)

        # Graph representation: adjacency list
        self.vertices = list(range(1, n + 1))  # Vertices numbered 1 to n
        self.edges = generator.generate(n, k, p)  # Create a bipartite graph
        # self.edges: Set[Tuple[int, int]] = set()
        self.independent_sets: List[List[int]] = [[] for _ in range(k)]
        self.vertex_to_set: dict = {}  # Maps vertex to its independent set index
        


    def get_online_ordering(self) -> List[int]:
        """
        Get the online ordering of vertices (random permutation).
        
        Returns:
            List of vertices in the order they will be revealed online
        """
        ordering = self.vertices.copy()
        random.shuffle(ordering)
        return ordering
    
    def get_edges_for_vertex(self, vertex: int, revealed_vertices: Set[int]) -> List[int]:
        """
        Get edges for a vertex that connect to already revealed vertices.
        
        Args:
            vertex: The vertex to get edges for
            revealed_vertices: Set of vertices already revealed
            
        Returns:
            List of neighbors that are already revealed
        """
        neighbors = []
        for edge in self.edges:
            if vertex in edge:
                other = edge[0] if edge[1] == vertex else edge[1]
                if other in revealed_vertices:
                    neighbors.append(other)
        return neighbors
    
    def save_to_edges_format(self, filename: str, ordering: List[int] = None):
        """
        Save graph to EDGES format file.
        
        Args:
            filename: Output filename
            ordering: Optional vertex ordering (if None, uses natural order)
        """
        with open(filename, 'w') as f:
            for u, v in self.edges:
                f.write(f"{u} {v}\n")
    
    @staticmethod
    def load_from_edges_format(filename: str) -> Tuple[List[int], Set[Tuple[int, int]], List[int]]:
        """
        Load graph from EDGES format file.
        
        Returns:
            Tuple of (vertices, edges, ordering)
        """
        vertices_set = set()
        edges = set()
        ordering = None
        header_processed = False
        
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    # Extract ordering from comment if present
                    if 'Vertex ordering:' in line:
                        ordering_str = line.split('Vertex ordering:')[1].strip()
                        ordering = [int(x) for x in ordering_str.split()]
                    continue
                
                parts = line.split()
                if len(parts) == 2:
                    try:
                        u, v = int(parts[0]), int(parts[1])
                        vertices_set.add(u)
                        vertices_set.add(v)
                        edges.add(tuple(sorted((u, v))))
                        header_processed = True
                    except ValueError:
                        continue
        
        vertices = sorted(vertices_set)
        
        if ordering is None:
            ordering = vertices.copy()
        
        return vertices, edges, ordering


def generate_multiple_graphs(n: int, k: int, p: float, N: int, 
                            output_dir: str = "graphs", seed: int = None) -> List[str]:
    """
    Generate N random k-colourable graphs and save them.
    
    Args:
        n: Number of vertices
        k: Chromatic number
        p: Edge probability
        N: Number of graphs to generate
        output_dir: Directory to save graphs
        seed: Random seed
        
    Returns:
        List of generated filenames
    """
    os.makedirs(output_dir, exist_ok=True)
    filenames = []
    
    for i in range(N):
        gen = GraphGenerator(n, k, p, seed=seed + i if seed is not None else None)
        ordering = gen.get_online_ordering()
        filename = os.path.join(output_dir, f"graph_n{n}_k{k}_p{p:.2f}_run{i+1}.edges")
        gen.save_to_edges_format(filename, ordering)
        filenames.append(filename)
    
    return filenames


if __name__ == "__main__":
    # Example usage
    gen = GraphGenerator(n=10, k=2, p=0.5, seed=42)
    ordering = gen.get_online_ordering()
    gen.save_to_edges_format("example_graph.edges", ordering)
    print(f"Generated graph with {gen.n} vertices, {len(gen.edges)} edges")
    print(f"Online ordering: {ordering}")