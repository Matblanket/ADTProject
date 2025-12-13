from typing import Dict, List, Set, Tuple, Callable, Optional
from collections import defaultdict,deque

class FirstFit:
   
    def __init__(self):
        self.coloring: Dict[int, int] = {}  
        self.num_colors = 0
   
    def color_vertex(self, vertex: int, neighbors: List[int]) -> int:
        mask = 0
        for neighbor in neighbors:
            if neighbor in self.coloring:
                c = self.coloring[neighbor]
                mask |= (1 << (c - 1)) 
       
        color = 1
        temp = mask
        while (temp & 1) == 1:
            temp >>= 1
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
        return self.num_colors


    def get_coloring(self) -> Dict[int, int]:
        return self.coloring.copy()


class CBIP:
   
    def __init__(self):
        self.coloring: Dict[int, int] = {}
        self.num_colors: int = 0


    def color_online_graph(self, ordering: List[int], get_neighbors_func) -> Dict[int, int]:
        self.coloring = {}
        self.num_colors = 0
        revealed: Set[int] = set()


        for v in ordering:
            self._color_vertex(v, revealed, get_neighbors_func)
            revealed.add(v)


        return self.coloring


    def _color_vertex(self, v: int, revealed: Set[int], get_neighbors_func):
        if not revealed:
            self.coloring[v] = 1
            self.num_colors = 1
            return
        CC = self._compute_connected_component(v, revealed, get_neighbors_func)
        A, B = self._bipartition(CC, v, get_neighbors_func)
        colors_in_B = {self.coloring[u] for u in B if u in self.coloring}
       
        color = 1
        while color in colors_in_B:
            color += 1


        self.coloring[v] = color
        self.num_colors = max(self.num_colors, color)


    def _compute_connected_component(self, v: int, revealed: Set[int], get_neighbors_func) -> Set[int]:
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
        partition = {root: 0}
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

    def __init__(self, chunk_size: int = 10):
        self.coloring: Dict[int, int] = {}
        self.num_colors = 0
        self.chunk_size = chunk_size


    def color_online_graph(self, vertices: List[int], get_neighbors_func) -> Dict[int, int]:
        self.coloring = {}
        self.num_colors = 0
       
        remaining = set(vertices)
        revealed: Set[int] = set()
       
        while remaining:
            min_degree = float('inf')
            next_vertex = None
           
            for v in remaining:
                degree_in_revealed = len([n for n in get_neighbors_func(v, revealed) if n in revealed])
                if degree_in_revealed < min_degree:
                    min_degree = degree_in_revealed
                    next_vertex = v
           
            if next_vertex is None:
                next_vertex = remaining.pop()
            else:
                remaining.remove(next_vertex)
           
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
