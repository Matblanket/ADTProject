"""
Graph Coloring Algorithms

This module implements FirstFit and CBIP algorithms for online graph coloring.
"""

from typing import Dict, List, Set, Tuple, Callable
from collections import defaultdict,deque


class FirstFit:
    """FirstFit greedy coloring algorithm."""
    
    def __init__(self):
        self.coloring: Dict[int, int] = {}  # vertex -> color
        self.num_colors = 0
    
    # def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
    #     """
    #     Color a vertex using FirstFit algorithm.
        
    #     Args:
    #         vertex: Vertex to color
    #         neighbors: List of already colored neighbors
            
    #     Returns:
    #         Color assigned to the vertex
    #     """
    #     # Get colors used by neighbors
    #     neighbor_colors = set()
    #     for neighbor in neighbors:
    #         if neighbor in self.coloring:
    #             neighbor_colors.add(self.coloring[neighbor])
        
    #     # Find the smallest color not used by neighbors
    #     color = 1
    #     while color in neighbor_colors:
    #         color += 1
        
    #     # Assign color to vertex
    #     self.coloring[vertex] = color
    #     self.num_colors = max(self.num_colors, color)
        
    #     return color

    def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
        neighbor_colors = 0  # Python ints have arbitrary precision, so no overflow!
        
        for neighbor in neighbors:
            if neighbor in self.coloring:
                color_val = self.coloring[neighbor]
                color_bit = 1 << (color_val - 1)
                neighbor_colors |= color_bit
        
        # Find first zero bit
        color = 1
        while neighbor_colors & 1:
            neighbor_colors >>= 1
            color += 1
        
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
    """
    CBIP (Coloring Based on Interval Partitioning) algorithm.
    Only for k = 2, as required by the project.
    """

    def __init__(self):
        self.coloring: Dict[int, int] = {}  # vertex -> color
        self.num_colors: int = 0
        self.partition_cache: Dict[int, int] = {}

    def _get_connected_component(
        self,
        start: int,
        revealed: Set[int],
        get_neighbors_func: Callable[[int, Set[int]], List[int]]
    ) -> Set[int]:
        """
        BFS to return the connected component containing start vertex,
        considering only revealed vertices.
        """
        CC = set([start])
        queue = deque([start])

        while queue:
            v = queue.popleft()
            neighbors = get_neighbors_func(v, revealed)
            for u in neighbors:
                if u not in CC:
                    CC.add(u)
                    queue.append(u)

        return CC

    def _bipartition(
        self,
        CC: Set[int],
        start: int,
        get_neighbors_func: Callable[[int, Set[int]], List[int]]
    ) -> (Set[int], Set[int]):
        """
        BFS to bipartition the connected component into two independent sets.
        start vertex is always in set A.
        """
        A, B = set(), set()
        partition: Dict[int, int] = {start: 0}  # 0 -> A, 1 -> B
        queue = deque([start])

        while queue:
            v = queue.popleft()
            side = partition[v]

            for u in get_neighbors_func(v, CC):
                if u not in partition:
                    partition[u] = 1 - side
                    queue.append(u)

        # Build sets
        for v, side in partition.items():
            if side == 0:
                A.add(v)
            else:
                B.add(v)

        return A, B

    def color_vertex(self, vertex: int, revealed: Set[int], get_neighbors_func) -> int:
        if not revealed:
            self.coloring[vertex] = 1
            self.partition_cache[vertex] = 0
            self.num_colors = 1
            return 1
        
        # Find conflicting partitions
        neighbor_partitions = set()
        for neighbor in get_neighbors_func(vertex, revealed):
            if neighbor in self.partition_cache:
                neighbor_partitions.add(self.partition_cache[neighbor])
        
        # Choose partition for new vertex (opposite of neighbors)
        if 0 in neighbor_partitions:
            vertex_partition = 1
        else:
            vertex_partition = 0
        
        self.partition_cache[vertex] = vertex_partition
        
        # Colors used in opposite partition
        used_colors = set()
        for v, part in self.partition_cache.items():
            if part != vertex_partition and v in self.coloring and v in revealed:
                used_colors.add(self.coloring[v])
        
        color = 1
        while color in used_colors:
            color += 1
        
        self.coloring[vertex] = color
        self.num_colors = max(self.num_colors, color)
        return color

    # def color_vertex(
    #     self,
    #     vertex: int,
    #     revealed: Set[int],
    #     get_neighbors_func: Callable[[int, Set[int]], List[int]]
    # ) -> int:
    #     """
    #     Color a vertex using the CBIP rule:
    #     - Compute connected component of vertex among revealed
    #     - Bipartition it into sets A (vertex's set) and B
    #     - Assign smallest color not used in B
    #     """
    #     if not revealed:
    #         # First vertex - color with 1
    #         self.coloring[vertex] = 1
    #         self.num_colors = max(self.num_colors, 1)
    #         return 1

    #     # REMOVE THIS LINE: CC.add(vertex) - DON'T include current vertex in CC
    #     # Get connected component ONLY from revealed vertices
    #     CC = self._get_connected_component(vertex, revealed, get_neighbors_func)

    #     if not CC:
    #         # No connected component found - color with 1
    #         self.coloring[vertex] = 1
    #         self.num_colors = max(self.num_colors, 1)
    #         return 1

    #     # Bipartition the connected component (only revealed vertices)
    #     # Start with any vertex in CC
    #     start_vertex = next(iter(CC))
    #     A, B = self._bipartition(CC, start_vertex, get_neighbors_func)

    #     # Determine which partition the NEW vertex belongs to
    #     vertex_neighbors = set(get_neighbors_func(vertex, revealed))
        
    #     # If vertex has neighbors in A, it should go to B's "side"
    #     if vertex_neighbors & A:
    #         # Vertex belongs to B's partition, so we avoid colors used in A
    #         used_colors = {self.coloring[v] for v in A if v in self.coloring}
    #     else:
    #         # Vertex belongs to A's partition, so we avoid colors used in B  
    #         used_colors = {self.coloring[v] for v in B if v in self.coloring}

    #     # Find smallest color not used in the opposite partition
    #     color = 1
    #     while color in used_colors:
    #         color += 1

    #     self.coloring[vertex] = color
    #     self.num_colors = max(self.num_colors, color)
    #     return color

    def color_online_graph(
        self,
        ordering: List[int],
        get_neighbors_func: Callable[[int, Set[int]], List[int]]
    ) -> Dict[int, int]:
        """
        Color the graph in online order.
        """
        self.coloring = {}
        self.num_colors = 0
        revealed: Set[int] = set()

        for v in ordering:
            self.color_vertex(v, revealed, get_neighbors_func)
            revealed.add(v)

        return self.coloring

    def get_num_colors(self) -> int:
        return self.num_colors


class FirstFitHeuristic:
    """
    FIXED: True online heuristic - reorder based on CURRENT degree (revealed neighbors only)
    """
    
    def __init__(self):
        self.coloring: Dict[int, int] = {}
        self.num_colors = 0
        self.current_degrees: Dict[int, int] = {}
    
    # def _get_next_vertex_by_current_degree(
    #     self, 
    #     remaining_vertices: Set[int], 
    #     revealed: Set[int],
    #     get_neighbors_func
    # ) -> int:
    #     """
    #     Select the vertex with highest CURRENT degree (number of revealed neighbors).
    #     """
    #     max_degree = -1
    #     selected_vertex = None
        
    #     for vertex in remaining_vertices:
    #         current_neighbors = get_neighbors_func(vertex, revealed)
    #         current_degree = len(current_neighbors)
            
    #         if current_degree > max_degree:
    #             max_degree = current_degree
    #             selected_vertex = vertex
        
    #     return selected_vertex

    def _get_next_vertex_by_current_degree(
        self, 
        remaining_vertices: Set[int]
    ) -> int:
        if not self.current_degrees:
            return None
        return max(remaining_vertices, key=lambda v: self.current_degrees.get(v, -1))
    
    def _update_degrees_after_coloring(
        self,
        vertex: int,
        revealed: Set[int],
        get_neighbors_func
    ):
        """
        Update degree counts after adding a new vertex.
        """
        # Initialize degree for the new vertex
        self.current_degrees[vertex] = 0
        
        # Update degrees of neighbors
        neighbors = get_neighbors_func(vertex, revealed)
        for neighbor in neighbors:
            if neighbor in self.current_degrees:
                self.current_degrees[neighbor] += 1
            else:
                self.current_degrees[neighbor] = 1

    def _firstfit_color_vertex(self, vertex: int, neighbors: List[int]) -> int:
        """Color a vertex using FirstFit on revealed neighbors."""
        neighbor_colors = {self.coloring[n] for n in neighbors if n in self.coloring}
        color = 1
        while color in neighbor_colors:
            color += 1
        self.coloring[vertex] = color
        self.num_colors = max(self.num_colors, color)
        return color

    def color_online_graph(
        self,
        vertices: List[int],
        get_neighbors_func
    ) -> Dict[int, int]:
        self.coloring = {}
        self.num_colors = 0
        self.current_degrees = {}
        
        remaining_vertices = set(vertices)
        revealed: Set[int] = set()
        
        # Initialize degrees for all vertices
        for vertex in vertices:
            self.current_degrees[vertex] = 0
        
        while remaining_vertices:
            # Select vertex with highest current degree
            next_vertex = self._get_next_vertex_by_current_degree(remaining_vertices)
            
            if next_vertex is None:
                # Fallback: pick any vertex
                next_vertex = next(iter(remaining_vertices))
                
            # Color the vertex
            neighbors = get_neighbors_func(next_vertex, revealed)
            
            # Use your optimized FirstFit with bitmask
            neighbor_colors = 0
            for neighbor in neighbors:
                if neighbor in self.coloring:
                    color_bit = 1 << (self.coloring[neighbor] - 1)
                    neighbor_colors |= color_bit
            
            color = 1
            while neighbor_colors & 1:
                neighbor_colors >>= 1
                color += 1
            
            self.coloring[next_vertex] = color
            self.num_colors = max(self.num_colors, color)
            
            # Update degrees for remaining vertices
            self._update_degrees_after_coloring(next_vertex, revealed, get_neighbors_func)
            
            # Update sets
            revealed.add(next_vertex)
            remaining_vertices.remove(next_vertex)
        
        return self.coloring
    
    # def color_online_graph(
    #     self,
    #     vertices: List[int],
    #     get_neighbors_func
    # ) -> Dict[int, int]:
    #     """
    #     FIXED: True online coloring with degree-based heuristic.
    #     No longer requires all_edges upfront.
        
    #     Args:
    #         vertices: List of vertices in natural order
    #         get_neighbors_func: Function(vertex, revealed_vertices) -> List[neighbors]
        
    #     Returns:
    #         Coloring dictionary
    #     """
    #     self.coloring = {}
    #     self.num_colors = 0
        
    #     remaining_vertices = set(vertices)
    #     revealed: Set[int] = set()
        
    #     while remaining_vertices:
    #         # Select vertex with highest current degree
    #         next_vertex = self._get_next_vertex_by_current_degree(
    #             remaining_vertices, revealed, get_neighbors_func
    #         )
            
    #         if next_vertex is None:
    #             break
                
    #         # Color the selected vertex
    #         neighbors = get_neighbors_func(next_vertex, revealed)
    #         self._firstfit_color_vertex(next_vertex, neighbors)
            
    #         # Update sets
    #         revealed.add(next_vertex)
    #         remaining_vertices.remove(next_vertex)
        
    #     return self.coloring
    
    def get_num_colors(self) -> int:
        return self.num_colors