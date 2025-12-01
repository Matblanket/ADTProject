import random
import os
from typing import List, Tuple, Set
from multiprocessing import Pool


class GraphGenerator:
    """Generates random k-colourable online graphs."""
    
    def __init__(self, n: int, k: int, p: float, seed: int = None):
        self.n = n
        self.k = k
        self.p = p
        if seed is not None:
            random.seed(seed)
       
        self.vertices = list(range(1, n + 1))
        self.edges: Set[Tuple[int, int]] = set()
        self.independent_sets: List[Set[int]] = [set() for _ in range(k)]
        self.vertex_to_set: Dict[int, int] = {}
        self.adjacency_list: Dict[int, Set[int]] = {}
        
        self._generate_graph()
        self._build_adjacency_list()
        

    def _build_adjacency_list(self):
        self.adjacency_list = {v: set() for v in self.vertices}
        for u, v in self.edges:
            self.adjacency_list[u].add(v)
            self.adjacency_list[v].add(u)
    
    def get_online_ordering(self) -> List[int]:
        ordering = self.vertices.copy()
        random.shuffle(ordering)
        return ordering

    def get_edges_for_vertex(self, vertex: int, revealed_vertices: Set[int]) -> List[int]:
        if vertex not in self.adjacency_list:
            return []
        return [n for n in self.adjacency_list[vertex] if n in revealed_vertices]
        
    def save_to_edges_format(self, filename: str, ordering: List[int] = None):
        with open(filename, 'w') as f:
            if ordering:
                f.write(f"# Vertex ordering: {' '.join(map(str, ordering))}\n")
            
            for u, v in self.edges:
                f.write(f"{u} {v}\n")

    def _generate_graph(self):
        S = [set() for _ in range(self.k)]
        counter = 0
        
        for vertex in self.vertices:
            if counter < self.k:
                S[counter].add(vertex)
                self.vertex_to_set[vertex] = counter
                counter += 1
            else:
                set_idx = random.randint(0, self.k - 1)
                S[set_idx].add(vertex)
                self.vertex_to_set[vertex] = set_idx
        
        self.independent_sets = S
        
        for i in range(self.k):
            for vertex in S[i]:
                for j in range(i + 1, self.k):  # Avoid duplicate i,j and j,i
                    if not S[j]:  # Skip empty sets
                        continue
                        
                    # Ensure at least one edge between sets
                    other_vertex = random.choice(list(S[j]))
                    edge = tuple(sorted((vertex, other_vertex)))
                    self.edges.add(edge)
                    
                    # Add additional edges with probability p
                    for other in S[j]:
                        if other != other_vertex and random.random() < self.p:
                            edge = tuple(sorted((vertex, other)))
                            self.edges.add(edge)
    
    @staticmethod
    def load_from_edges_format(filename: str) -> Tuple[List[int], Set[Tuple[int, int]], List[int]]:
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

def generate_single_graph(args):
    i, n, k, p, output_dir, seed = args
    gen = GraphGenerator(n, k, p, seed=seed + i if seed is not None else None)
    ordering = gen.get_online_ordering()
    filename = os.path.join(output_dir, f"graph_n{n}_k{k}_p{p:.2f}_run{i+1}.edges")
    gen.save_to_edges_format(filename, ordering)
    return filename

def generate_multiple_graphs_parallel(n: int, k: int, p: float, N: int, 
                                    output_dir: str = "graphs", seed: int = None) -> List[str]:
    os.makedirs(output_dir, exist_ok=True)
    
    tasks = [(i, n, k, p, output_dir, seed) for i in range(N)] 
    
    with Pool() as pool:
        filenames = pool.map(generate_single_graph, tasks)
    
    return filenames


if __name__ == "__main__":
    # Example usage
    gen = GraphGenerator(n=10, k=2, p=0.5, seed=42)
    ordering = gen.get_online_ordering()
    gen.save_to_edges_format("example_graph.edges", ordering)
    print(f"Generated graph with {gen.n} vertices, {len(gen.edges)} edges")
    print(f"Online ordering: {ordering}")