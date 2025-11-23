"""
Graph Coloring Algorithms

This module implements FirstFit and CBIP algorithms for online graph coloring.
"""

from typing import Dict, List, Set, Tuple
from collections import defaultdict


class FirstFit:
    """FirstFit greedy coloring algorithm."""
    
    def __init__(self):
        self.coloring: Dict[int, int] = {}  # vertex -> color
        self.num_colors = 0
    
    def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
        """
        Color a vertex using FirstFit algorithm.
        
        Args:
            vertex: Vertex to color
            neighbors: List of already colored neighbors
            
        Returns:
            Color assigned to the vertex
        """
        # Get colors used by neighbors
        neighbor_colors = set()
        for neighbor in neighbors:
            if neighbor in self.coloring:
                neighbor_colors.add(self.coloring[neighbor])
        
        # Find the smallest color not used by neighbors
        color = 1
        while color in neighbor_colors:
            color += 1
        
        # Assign color to vertex
        self.coloring[vertex] = color
        self.num_colors = max(self.num_colors, color)
        
        return color
    
    def color_online_graph(self, vertices: List[int], 
                          get_neighbors_func) -> Dict[int, int]:
        """
        Color an online graph using FirstFit.
        
        Args:
            vertices: List of vertices in online order
            get_neighbors_func: Function(vertex, revealed_vertices) -> List[neighbors]
        
        Returns:
            Coloring dictionary
        """
        self.coloring = {}
        self.num_colors = 0
        revealed = set()
        
        for vertex in vertices:
            neighbors = get_neighbors_func(vertex, revealed)
            self.color_vertex(vertex, neighbors)
            revealed.add(vertex)
        
        return self.coloring
    
    def get_num_colors(self) -> int:
        """Get the number of colors used."""
        return self.num_colors


class CBIP:
    """CBIP (Coloring Based on Interval Partitioning) algorithm."""
    
    def __init__(self, k: int):
        """
        Initialize CBIP algorithm.
        
        Args:
            k: Chromatic number of the graph (number of independent sets)
        """
        self.k = k
        self.coloring: Dict[int, int] = {}
        self.num_colors = 0
    
    def _compute_k_partition(self, vertices: Set[int], 
                            get_neighbors_func) -> List[Set[int]]:
        """
        Compute a k-partition of vertices into k independent sets.
        Uses a greedy approach: assign each vertex to the first set
        where it has no neighbors.
        
        Args:
            vertices: Set of vertices to partition
            get_neighbors_func: Function(vertex, vertex_set) -> List[neighbors]
        
        Returns:
            List of k independent sets
        """
        partition = [set() for _ in range(self.k)]
        
        # Process vertices in some order (sorted for determinism)
        sorted_vertices = sorted(vertices)
        
        for vertex in sorted_vertices:
            # Try to assign vertex to first independent set where it fits
            assigned = False
            for i in range(self.k):
                # Check if vertex has neighbors in set i
                neighbors = get_neighbors_func(vertex, vertices)
                has_neighbor_in_set = any(neighbor in partition[i] 
                                        for neighbor in neighbors)
                
                if not has_neighbor_in_set:
                    partition[i].add(vertex)
                    assigned = True
                    break
            
            # If vertex couldn't be assigned to any set, assign to first set
            # (This shouldn't happen for k-colourable graphs, but handle it)
            if not assigned:
                partition[0].add(vertex)
        
        return partition
    
    def _find_vertex_set(self, vertex: int, partition: List[Set[int]]) -> int:
        """Find which independent set a vertex belongs to."""
        for i, s in enumerate(partition):
            if vertex in s:
                return i
        return 0  # Default to first set if not found
    
    def color_vertex(self, vertex: int, neighbors: List[int], 
                    current_vertices: Set[int], get_neighbors_func) -> int:
        """
        Color a vertex using CBIP algorithm.
        
        Args:
            vertex: Vertex to color
            neighbors: List of already colored neighbors
            current_vertices: Set of all currently revealed vertices
            get_neighbors_func: Function to get neighbors
        
        Returns:
            Color assigned to the vertex
        """
        # Include the new vertex in the set for partition computation
        vertices_with_new = current_vertices.copy()
        vertices_with_new.add(vertex)
        
        # Compute k-partition of current vertices (including new vertex)
        partition = self._compute_k_partition(vertices_with_new, get_neighbors_func)
        
        # Find which set A the vertex belongs to
        set_A_idx = self._find_vertex_set(vertex, partition)
        set_A = partition[set_A_idx]
        
        # Find colors used by vertices NOT in set A (excluding the new vertex)
        colors_outside_A = set()
        for v in current_vertices:
            if v not in set_A and v in self.coloring:
                colors_outside_A.add(self.coloring[v])
        
        # Find smallest color not used outside A
        color = 1
        while color in colors_outside_A:
            color += 1
        
        # Assign color to vertex
        self.coloring[vertex] = color
        self.num_colors = max(self.num_colors, color)
        
        return color
    
    def color_online_graph(self, vertices: List[int], 
                          get_neighbors_func) -> Dict[int, int]:
        """
        Color an online graph using CBIP.
        
        Args:
            vertices: List of vertices in online order
            get_neighbors_func: Function(vertex, revealed_vertices) -> List[neighbors]
        
        Returns:
            Coloring dictionary
        """
        self.coloring = {}
        self.num_colors = 0
        revealed = set()
        
        for vertex in vertices:
            neighbors = get_neighbors_func(vertex, revealed)
            self.color_vertex(vertex, neighbors, revealed, get_neighbors_func)
            revealed.add(vertex)
        
        return self.coloring
    
    def get_num_colors(self) -> int:
        """Get the number of colors used."""
        return self.num_colors


class FirstFitHeuristic:
    """
    Heuristic improvement for FirstFit.
    
    Strategy: Sort vertices by degree in non-increasing order before coloring.
    This is a common heuristic that often improves performance.
    """
    
    def __init__(self):
        self.coloring: Dict[int, int] = {}
        self.num_colors = 0
    
    def _get_degree_ordering(self, vertices: List[int], 
                           all_edges: Set[Tuple[int, int]]) -> List[int]:
        """
        Get vertices sorted by degree in non-increasing order.
        
        Args:
            vertices: All vertices
            all_edges: All edges in the graph
        
        Returns:
            Vertices sorted by degree (highest first)
        """
        # Calculate degrees
        degrees = defaultdict(int)
        for u, v in all_edges:
            degrees[u] += 1
            degrees[v] += 1
        
        # Sort by degree (non-increasing)
        sorted_vertices = sorted(vertices, key=lambda v: degrees[v], reverse=True)
        return sorted_vertices
    
    def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
        """Color a vertex using FirstFit (same as base FirstFit)."""
        neighbor_colors = set()
        for neighbor in neighbors:
            if neighbor in self.coloring:
                neighbor_colors.add(self.coloring[neighbor])
        
        color = 1
        while color in neighbor_colors:
            color += 1
        
        self.coloring[vertex] = color
        self.num_colors = max(self.num_colors, color)
        
        return color
    
    def color_online_graph(self, vertices: List[int], 
                          all_edges: Set[Tuple[int, int]],
                          get_neighbors_func) -> Dict[int, int]:
        """
        Color an online graph using FirstFit with degree-based ordering.
        
        Args:
            vertices: All vertices
            all_edges: All edges in the graph
            get_neighbors_func: Function(vertex, revealed_vertices) -> List[neighbors]
        
        Returns:
            Coloring dictionary
        """
        self.coloring = {}
        self.num_colors = 0
        
        # Reorder vertices by degree
        ordered_vertices = self._get_degree_ordering(vertices, all_edges)
        
        revealed = set()
        for vertex in ordered_vertices:
            neighbors = get_neighbors_func(vertex, revealed)
            self.color_vertex(vertex, neighbors)
            revealed.add(vertex)
        
        return self.coloring
    
    def get_num_colors(self) -> int:
        """Get the number of colors used."""
        return self.num_colors

