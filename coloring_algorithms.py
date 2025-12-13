# """
# Graph Coloring Algorithms

# This module implements FirstFit and CBIP algorithms for online graph coloring.
# """

# from typing import Dict, List, Set, Tuple, Callable
# from collections import defaultdict,deque


# class FirstFit:
#     """FirstFit greedy coloring algorithm."""
    
#     def __init__(self):
#         self.coloring: Dict[int, int] = {}  
#         self.num_colors = 0
    
#     def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
#         used_colors = set()
#         for neighbor in neighbors:
#             if neighbor in self.coloring:
#                 used_colors.add(self.coloring[neighbor])
#         color = 1
#         while color in used_colors:
#             color += 1
#         self.coloring[vertex] = color
#         if color > self.num_colors:
#             self.num_colors = color
#         return color
    
#     def color_online_graph(self, vertices: List[int], 
#                           get_neighbors_func) -> Dict[int, int]:
        
#         self.coloring = {}
#         self.num_colors = 0
#         revealed = set()
        
#         for vertex in vertices:
#             neighbors = get_neighbors_func(vertex, revealed)
#             self.color_vertex(vertex, neighbors)
#             revealed.add(vertex)
        
#         return self.coloring
    
#     def get_num_colors(self) -> int:
#         """Get the number of colors used."""
#         return self.num_colors

#     def get_coloring(self) -> Dict[int, int]:
#         """Get the complete coloring."""
#         return self.coloring.copy()


# from typing import Dict, Set, List, Callable, Optional
# from collections import deque

# # Note: Assuming 'Dict' and 'Set' are imported from 'typing' as shown above
# class CBIP:
#    def __init__(self):
#        self.coloring: Dict[int, int] = {}
#        self.num_colors: int = 0

#    def _get_connected_component(self, vertex: int, revealed: Set[int], get_neighbors_func):
#        """Find connected component containing vertex in revealed graph."""
#        if vertex not in revealed:
#            return set()
          
#        component = set()
#        queue = deque([vertex])
#        while queue:
#            v = queue.popleft()
#            if v not in component:
#                component.add(v)
#                for neighbor in get_neighbors_func(v, revealed):
#                    if neighbor not in component:
#                        queue.append(neighbor)
#        return component

#    def _bipartition_component(self, component: Set[int], get_neighbors_func):
#        """Bipartition a connected component."""
#        if not component:
#            return set(), set()
          
#        start = next(iter(component))
#        A, B = set(), set()
#        partition = {start: 0}
#        queue = deque([start])
      
#        while queue:
#            v = queue.popleft()
#            current_partition = partition[v]
          
#            for neighbor in get_neighbors_func(v, component):
#                if neighbor not in partition:
#                    partition[neighbor] = 1 - current_partition
#                    queue.append(neighbor)
#                elif partition[neighbor] == current_partition:
#                    # Should not happen in bipartite graphs
#                    pass
      
#        for v, part in partition.items():
#            if part == 0:
#                A.add(v)
#            else:
#                B.add(v)
              
#        return A, B

#    def color_vertex(self, vertex: int, revealed: Set[int], get_neighbors_func) -> int:
#        if not revealed:
#            self.coloring[vertex] = 1
#            self.num_colors = 1
#            return 1

#        # Get connected component in revealed graph
#        component = self._get_connected_component(vertex, revealed, get_neighbors_func)
      
#        if not component:
#            # No connected vertices - use color 1
#            color = 1
#        else:
#            # Bipartition the component
#            A, B = self._bipartition_component(component, get_neighbors_func)
          
#            # Determine which partition vertex belongs to by checking neighbors
#            vertex_in_A = True
#            for neighbor in get_neighbors_func(vertex, revealed):
#                if neighbor in A:
#                    vertex_in_A = False
#                    break
          
#            # Color with smallest color not used in opposite partition
#            if vertex_in_A:
#                used_colors = set(self.coloring.get(v, 0) for v in B if v in self.coloring)
#            else:
#                used_colors = set(self.coloring.get(v, 0) for v in A if v in self.coloring)
          
#            color = 1
#            while color in used_colors:
#                color += 1

#        self.coloring[vertex] = color
#        self.num_colors = max(self.num_colors, color)
#        return color

#    def color_online_graph(self, ordering: List[int], get_neighbors_func) -> Dict[int, int]:
#        self.coloring = {}
#        self.num_colors = 0
#        revealed: Set[int] = set()

#        for v in ordering:
#            self.color_vertex(v, revealed, get_neighbors_func)
#            revealed.add(v)

#        return self.coloring

#    def get_num_colors(self) -> int:
#        return self.num_colors


# class FirstFitHeuristic:

#     def __init__(self, chunk_size: int = 50):
#         self.coloring: Dict[int, int] = {}
#         self.num_colors = 0
#         self.chunk_size = chunk_size

#     def color_online_graph(self, vertices: List[int], get_neighbors_func) -> Dict[int, int]:
#         self.coloring = {}
#         self.num_colors = 0
#         remaining_vertices = set(vertices)
#         revealed: Set[int] = set()
        
#         while remaining_vertices:
#             chunk = list(remaining_vertices)[:self.chunk_size]
#             next_vertex = min(chunk, key=lambda v: len(get_neighbors_func(v, revealed)))
#             neighbors = get_neighbors_func(next_vertex, revealed)
#             used_colors = set()
#             for neighbor in neighbors:
#                 if neighbor in self.coloring:
#                     used_colors.add(self.coloring[neighbor])
            
#             color = 1
#             while color in used_colors:
#                 color += 1
            
#             self.coloring[next_vertex] = color
#             self.num_colors = max(self.num_colors, color)
            
#             revealed.add(next_vertex)
#             remaining_vertices.remove(next_vertex)
        
#         return self.coloring

#     def get_num_colors(self) -> int:
#         return self.num_colors
    

from typing import Dict, List, Set, Tuple, Callable
from collections import defaultdict,deque


class FirstFit:
    """FirstFit greedy coloring algorithm."""
   
    def __init__(self):
        self.coloring: Dict[int, int] = {}  
        self.num_colors = 0
   
    def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
        used_colors = set()
        for neighbor in neighbors:
            if neighbor in self.coloring:
                used_colors.add(self.coloring[neighbor])
        color = 1
        while color in used_colors:
            color += 1
        self.coloring[vertex] = color
        if color > self.num_colors:
            self.num_colors = color
        return color
   
    def color_online_graph(self, vertices: List[int],
                          get_neighbors_func) -> Dict[int, int]:
       
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

    def get_coloring(self) -> Dict[int, int]:
        """Get the complete coloring."""
        return self.coloring.copy()


from typing import Dict, Set, List, Callable, Optional
from collections import deque

class CBIP:
    """CBIP algorithm for k=2 (bipartite graphs) - achieves optimal competitive ratio."""
   
    def __init__(self):
        self.coloring: Dict[int, int] = {}
        self.num_colors: int = 0

    def color_online_graph(self, ordering: List[int], get_neighbors_func) -> Dict[int, int]:
        """Color entire graph in online fashion."""
        self.coloring = {}
        self.num_colors = 0
        revealed: Set[int] = set()

        for v in ordering:
            self._color_vertex(v, revealed, get_neighbors_func)
            revealed.add(v)

        return self.coloring

    def _color_vertex(self, v: int, revealed: Set[int], get_neighbors_func):
        """Color vertex v according to CBIP algorithm."""
        if not revealed:
            self.coloring[v] = 1
            self.num_colors = 1
            return

        # Step 1: Compute connected component CC of v in revealed graph
        CC = self._compute_connected_component(v, revealed, get_neighbors_func)

        # Step 2: Bipartition CC so that v is in partition A
        A, B = self._bipartition(CC, v, get_neighbors_func)

        # Step 3: Color v using smallest color NOT in B
        colors_in_B = {self.coloring[u] for u in B if u in self.coloring}
       
        color = 1
        while color in colors_in_B:
            color += 1

        self.coloring[v] = color
        self.num_colors = max(self.num_colors, color)

    def _compute_connected_component(self, v: int, revealed: Set[int], get_neighbors_func) -> Set[int]:
        """Find connected component of v in the partially revealed graph."""
        CC = set()
        queue = deque([v])
        visited = set()

        while queue:
            x = queue.popleft()
            if x in visited:
                continue
            visited.add(x)
            CC.add(x)

            for nbr in get_neighbors_func(x, revealed):
                if nbr not in visited:
                    queue.append(nbr)

        return CC

    def _bipartition(self, CC: Set[int], root: int, get_neighbors_func) -> Tuple[Set[int], Set[int]]:
        """Bipartition CC into A and B such that root (v) belongs to A."""
        partition = {root: 0}  # 0 = A, 1 = B
        queue = deque([root])

        while queue:
            u = queue.popleft()
            current_side = partition[u]

            for nbr in get_neighbors_func(u, CC):
                if nbr not in partition:
                    partition[nbr] = 1 - current_side
                    queue.append(nbr)

        A = {x for x in CC if partition[x] == 0}
        B = {x for x in CC if partition[x] == 1}

        return A, B

    def get_num_colors(self) -> int:
        return self.num_colors


class FirstFitHeuristic:
    """FirstFit with minimum-degree-first heuristic in revealed subgraph."""

    def __init__(self, chunk_size: int = 10):
        self.coloring: Dict[int, int] = {}
        self.num_colors = 0
        self.chunk_size = chunk_size

    def color_online_graph(self, vertices: List[int], get_neighbors_func) -> Dict[int, int]:
        self.coloring = {}
        self.num_colors = 0
       
        remaining = set(vertices)
        revealed: Set[int] = set()
       
        # Process vertices in chunks, selecting minimum degree in revealed subgraph
        while remaining:
            # Select next vertex: minimum degree among unrevealed vertices in revealed subgraph
            min_degree = float('inf')
            next_vertex = None
           
            for v in remaining:
                # Count edges to already revealed vertices
                degree_in_revealed = len([n for n in get_neighbors_func(v, revealed) if n in revealed])
                if degree_in_revealed < min_degree:
                    min_degree = degree_in_revealed
                    next_vertex = v
           
            if next_vertex is None:
                next_vertex = remaining.pop()
            else:
                remaining.remove(next_vertex)
           
            # Color using FirstFit
            neighbors = get_neighbors_func(next_vertex, revealed)
            used_colors = {self.coloring[n] for n in neighbors if n in self.coloring}
           
            color = 1
            while color in used_colors:
                color += 1
           
            self.coloring[next_vertex] = color
            self.num_colors = max(self.num_colors, color)
            revealed.add(next_vertex)
       
        return self.coloring

    def get_num_colors(self) -> int:
        return self.num_colors
