import os
import statistics
from typing import Dict, List, Set, Callable, Tuple
from graph_generator import GraphGenerator
from coloring_algorithms import FirstFit, CBIP, FirstFitHeuristic
from multiprocessing import Pool
from collections import deque
from tqdm import tqdm 
from graph_generator import generate_multiple_graphs_parallel

class SimulationRunner:
    def __init__(self):
        self.results = []
        self.adjacency_cache: Dict[Tuple[int, int], Dict[int, Set[int]]] = {}

    def build_adjacency_dict(self, vertices: List[int], edges: Set[Tuple[int, int]]) -> Dict[int, Set[int]]:
        cache_key = (len(vertices), hash(frozenset(edges)))
        
        if cache_key not in self.adjacency_cache:
            adj = {v: set() for v in vertices}
            for u, v in edges:
                adj[u].add(v)
                adj[v].add(u)
            self.adjacency_cache[cache_key] = adj
        
        return self.adjacency_cache[cache_key]

    def get_neighbors(self, vertex: int, revealed: Set[int], adj: Dict[int, Set[int]]) -> List[int]:
        return list(adj[vertex] & revealed)

    def color_single_graph(self, n: int, k: int, p: float,
                           algorithm_name: str, vertices: List[int],
                           edges: Set[Tuple[int, int]], ordering: List[int]) -> Dict:
        adj = self.build_adjacency_dict(vertices, edges)

        if algorithm_name == 'FirstFit':
            algorithm = FirstFit()
            coloring = algorithm.color_online_graph(ordering, lambda v, r: self.get_neighbors(v, r, adj))
            num_colors = algorithm.get_num_colors()

        elif algorithm_name == 'CBIP':
            algorithm = CBIP()
            coloring = algorithm.color_online_graph(ordering, lambda v, r: self.get_neighbors(v, r, adj))
            num_colors = algorithm.get_num_colors()

        elif algorithm_name == 'FirstFitHeuristic':
            algorithm = FirstFitHeuristic()
            coloring = algorithm.color_online_graph(ordering, lambda v, r: self.get_neighbors(v, r, adj))
            num_colors = algorithm.get_num_colors()
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")

        return {
            'num_colors': num_colors,
            'chromatic_number': k,
            'competitive_ratio': num_colors / k,
            'coloring': coloring
        }

    def run_single_experiment(self, n: int, k: int, p: float,
                              algorithm_name: str, graph_file: str = None, seed: int = None) -> Dict:
        if graph_file and os.path.exists(graph_file):
            vertices, edges, ordering = GraphGenerator.load_from_edges_format(graph_file)
        else:
            gen = GraphGenerator(n, k, p, seed=seed)
            vertices = gen.vertices
            edges = gen.edges
            ordering = gen.get_online_ordering()

        result = self.color_single_graph(n, k, p, algorithm_name, vertices, edges, ordering)
        result.update({'n': n, 'k': k, 'p': p, 'algorithm': algorithm_name})
        return result

    def run_batch_experiments(self, n: int, k: int, p: float, N: int,
                              algorithm_name: str, graph_files: List[str] = None,
                              seed: int = None, parallel: bool = False) -> Dict:
        tasks = []
        for i in range(N):
            graph_file = graph_files[i] if graph_files else None
            current_seed = seed + i if seed is not None else None
            tasks.append((n, k, p, algorithm_name, graph_file, current_seed))

        if parallel:
            with Pool() as pool:
                results = list(tqdm(pool.imap(self.run_single_experiment_unpack, tasks), 
                                total=len(tasks), desc=f"n={n}, k={k}"))
        else:
            results = []
            for task in tqdm(tasks, desc=f"n={n}, k={k}"):
                results.append(self.run_single_experiment(*task))

        competitive_ratios = [r['competitive_ratio'] for r in results]
        return {
            'n': n,
            'k': k,
            'N': N,
            'algorithm': algorithm_name,
            'avg_competitive_ratio': statistics.mean(competitive_ratios),
            'std_dev': statistics.stdev(competitive_ratios) if len(competitive_ratios) > 1 else 0.0,
            'competitive_ratios': competitive_ratios
        }

    def run_single_experiment_unpack(self, args):
        return self.run_single_experiment(*args)

    def generate_all_graphs(self, n_values: list, k_values: list, p: float, N: int, 
                        output_dir: str, seed: int = None):
        
        total_graphs = len(n_values) * len(k_values) * N
        graph_count = 0
        
        for n in n_values:
            for k in k_values:
                print(f"Generating {N} graphs with n={n}, k={k}...")
                generate_multiple_graphs_parallel(n, k, p, N, output_dir, seed)
                graph_count += N
        
        print(f"Generated {graph_count} total graphs in {output_dir}/")

    def run_full_simulation(self, n_values: list, k_values: list, p: float, N: int,
                        algorithm_name: str, graph_dir: str, seed: int = None) -> list:

        
        results = []
        
        for n in n_values:
            for k in k_values:
                print(f"  Running {algorithm_name} on n={n}, k={k}...")
                
                graph_files = []
                for i in range(N):
                    filename = f"graph_n{n}_k{k}_p{p:.2f}_run{i+1}.edges"
                    graph_files.append(os.path.join(graph_dir, filename))
                
                batch_result = self.run_batch_experiments(
                    n=n, k=k, p=p, N=N, 
                    algorithm_name=algorithm_name,
                    graph_files=graph_files,
                    seed=seed
                )
                results.append(batch_result)
                print(f"    Average competitive ratio: {batch_result['avg_competitive_ratio']:.4f}")
        
        return results

    
