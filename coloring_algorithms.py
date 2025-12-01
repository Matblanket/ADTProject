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

# Note: Assuming 'Dict' and 'Set' are imported from 'typing' as shown above
class CBIP:
   def __init__(self):
       self.coloring: Dict[int, int] = {}
       self.num_colors: int = 0

   def _get_connected_component(self, vertex: int, revealed: Set[int], get_neighbors_func):
       """Find connected component containing vertex in revealed graph."""
       if vertex not in revealed:
           return set()
          
       component = set()
       queue = deque([vertex])
       while queue:
           v = queue.popleft()
           if v not in component:
               component.add(v)
               for neighbor in get_neighbors_func(v, revealed):
                   if neighbor not in component:
                       queue.append(neighbor)
       return component

   def _bipartition_component(self, component: Set[int], get_neighbors_func):
       """Bipartition a connected component."""
       if not component:
           return set(), set()
          
       start = next(iter(component))
       A, B = set(), set()
       partition = {start: 0}
       queue = deque([start])
      
       while queue:
           v = queue.popleft()
           current_partition = partition[v]
          
           for neighbor in get_neighbors_func(v, component):
               if neighbor not in partition:
                   partition[neighbor] = 1 - current_partition
                   queue.append(neighbor)
               elif partition[neighbor] == current_partition:
                   # Should not happen in bipartite graphs
                   pass
      
       for v, part in partition.items():
           if part == 0:
               A.add(v)
           else:
               B.add(v)
              
       return A, B

   def color_vertex(self, vertex: int, revealed: Set[int], get_neighbors_func) -> int:
       if not revealed:
           self.coloring[vertex] = 1
           self.num_colors = 1
           return 1

       # Get connected component in revealed graph
       component = self._get_connected_component(vertex, revealed, get_neighbors_func)
      
       if not component:
           # No connected vertices - use color 1
           color = 1
       else:
           # Bipartition the component
           A, B = self._bipartition_component(component, get_neighbors_func)
          
           # Determine which partition vertex belongs to by checking neighbors
           vertex_in_A = True
           for neighbor in get_neighbors_func(vertex, revealed):
               if neighbor in A:
                   vertex_in_A = False
                   break
          
           # Color with smallest color not used in opposite partition
           if vertex_in_A:
               used_colors = set(self.coloring.get(v, 0) for v in B if v in self.coloring)
           else:
               used_colors = set(self.coloring.get(v, 0) for v in A if v in self.coloring)
          
           color = 1
           while color in used_colors:
               color += 1

       self.coloring[vertex] = color
       self.num_colors = max(self.num_colors, color)
       return color

   def color_online_graph(self, ordering: List[int], get_neighbors_func) -> Dict[int, int]:
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

    def __init__(self, chunk_size: int = 50):
        self.coloring: Dict[int, int] = {}
        self.num_colors = 0
        self.chunk_size = chunk_size

    def color_online_graph(self, vertices: List[int], get_neighbors_func) -> Dict[int, int]:
        self.coloring = {}
        self.num_colors = 0
        remaining_vertices = set(vertices)
        revealed: Set[int] = set()
        
        while remaining_vertices:
            chunk = list(remaining_vertices)[:self.chunk_size]
            next_vertex = min(chunk, key=lambda v: len(get_neighbors_func(v, revealed)))
            neighbors = get_neighbors_func(next_vertex, revealed)
            used_colors = set()
            for neighbor in neighbors:
                if neighbor in self.coloring:
                    used_colors.add(self.coloring[neighbor])
            
            color = 1
            while color in used_colors:
                color += 1
            
            self.coloring[next_vertex] = color
            self.num_colors = max(self.num_colors, color)
            
            revealed.add(next_vertex)
            remaining_vertices.remove(next_vertex)
        
        return self.coloring

    def get_num_colors(self) -> int:
        return self.num_colors
    