"""
Simulation Framework for Online Graph Coloring Experiments

This module runs experiments and calculates metrics like competitive ratio,
average competitive ratio, and standard deviation.
"""

import os
import statistics
from typing import Dict, List, Tuple, Set, Callable
from graph_generator import GraphGenerator
from coloring_algorithms import FirstFit, CBIP, FirstFitHeuristic


class SimulationRunner:
    """Runs simulations and calculates metrics."""
    
    def __init__(self):
        self.results = []
    
    def run_single_experiment(self, n: int, k: int, p: float, 
                             algorithm_name: str, algorithm_func: Callable,
                             graph_file: str = None, seed: int = None) -> Dict:
        """
        Run a single experiment on one graph.
        
        Args:
            n: Number of vertices
            k: Chromatic number
            p: Edge probability
            algorithm_name: Name of algorithm ('FirstFit', 'CBIP', 'FirstFitHeuristic')
            algorithm_func: Function that takes (vertices, edges, ordering) and returns num_colors
            graph_file: Optional graph file to load
            seed: Random seed
        
        Returns:
            Dictionary with experiment results
        """
        # Generate or load graph
        if graph_file and os.path.exists(graph_file):
            vertices, edges, ordering = GraphGenerator.load_from_edges_format(graph_file)
        else:
            gen = GraphGenerator(n, k, p, seed=seed)
            gen.generate()
            vertices = gen.vertices
            edges = gen.edges
            ordering = gen.get_online_ordering()
        
        # Create neighbor function
        def get_neighbors(vertex: int, revealed: Set[int]) -> List[int]:
            """Get neighbors of vertex that are in revealed set."""
            neighbors = []
            for edge in edges:
                if vertex in edge:
                    other = edge[0] if edge[1] == vertex else edge[1]
                    if other in revealed:
                        neighbors.append(other)
            return neighbors
        
        # Run algorithm
        if algorithm_name == 'FirstFit':
            algorithm = FirstFit()
            coloring = algorithm.color_online_graph(ordering, get_neighbors)
            num_colors = algorithm.get_num_colors()
        
        elif algorithm_name == 'CBIP':
            algorithm = CBIP(k)
            coloring = algorithm.color_online_graph(ordering, get_neighbors)
            num_colors = algorithm.get_num_colors()
        
        elif algorithm_name == 'FirstFitHeuristic':
            algorithm = FirstFitHeuristic()
            coloring = algorithm.color_online_graph(vertices, edges, get_neighbors)
            num_colors = algorithm.get_num_colors()
        
        else:
            raise ValueError(f"Unknown algorithm: {algorithm_name}")
        
        # Calculate competitive ratio
        competitive_ratio = num_colors / k  # k is the chromatic number
        
        result = {
            'n': n,
            'k': k,
            'p': p,
            'algorithm': algorithm_name,
            'num_colors': num_colors,
            'chromatic_number': k,
            'competitive_ratio': competitive_ratio,
            'coloring': coloring
        }
        
        return result
    
    def run_batch_experiments(self, n: int, k: int, p: float, N: int,
                             algorithm_name: str, graph_files: List[str] = None,
                             seed: int = None) -> Dict:
        """
        Run N experiments and calculate statistics.
        
        Args:
            n: Number of vertices
            k: Chromatic number
            p: Edge probability
            N: Number of graphs to test
            algorithm_name: Name of algorithm
            graph_files: Optional list of graph files to use
            seed: Random seed
        
        Returns:
            Dictionary with aggregated results
        """
        competitive_ratios = []
        
        for i in range(N):
            graph_file = graph_files[i] if graph_files else None
            current_seed = seed + i if seed is not None else None
            
            result = self.run_single_experiment(
                n, k, p, algorithm_name, None, graph_file, current_seed
            )
            competitive_ratios.append(result['competitive_ratio'])
        
        # Calculate statistics
        avg_competitive_ratio = statistics.mean(competitive_ratios)
        std_dev = statistics.stdev(competitive_ratios) if len(competitive_ratios) > 1 else 0.0
        
        return {
            'n': n,
            'k': k,
            'N': N,
            'algorithm': algorithm_name,
            'avg_competitive_ratio': avg_competitive_ratio,
            'std_dev': std_dev,
            'competitive_ratios': competitive_ratios
        }
    
    def run_full_simulation(self, n_values: List[int], k_values: List[int],
                           p: float, N: int, algorithm_name: str,
                           graph_dir: str = "graphs", seed: int = 42) -> List[Dict]:
        """
        Run full simulation for multiple n and k values.
        
        Args:
            n_values: List of vertex counts
            k_values: List of chromatic numbers
            p: Edge probability
            N: Number of graphs per configuration
            algorithm_name: Name of algorithm
            graph_dir: Directory containing graph files
            seed: Random seed
        
        Returns:
            List of result dictionaries
        """
        results = []
        
        for k in k_values:
            for n in n_values:
                # Try to load existing graphs
                graph_files = []
                for i in range(N):
                    graph_file = os.path.join(
                        graph_dir, f"graph_n{n}_k{k}_p{p:.2f}_run{i+1}.edges"
                    )
                    if os.path.exists(graph_file):
                        graph_files.append(graph_file)
                    else:
                        graph_files.append(None)
                
                # Run batch experiments
                batch_result = self.run_batch_experiments(
                    n, k, p, N, algorithm_name, graph_files, seed
                )
                results.append(batch_result)
                
                print(f"Completed: {algorithm_name}, k={k}, n={n}, "
                      f"avg_ρ={batch_result['avg_competitive_ratio']:.4f}")
        
        return results


def generate_all_graphs(n_values: List[int], k_values: List[int], 
                       p: float, N: int, output_dir: str = "graphs", 
                       seed: int = 42):
    """
    Generate all graphs needed for experiments.
    
    Args:
        n_values: List of vertex counts
        k_values: List of chromatic numbers
        p: Edge probability
        N: Number of graphs per configuration
        output_dir: Output directory
        seed: Random seed
    """
    from graph_generator import generate_multiple_graphs
    
    for k in k_values:
        for n in n_values:
            print(f"Generating graphs: k={k}, n={n}, N={N}")
            generate_multiple_graphs(n, k, p, N, output_dir, seed=seed)


if __name__ == "__main__":
    # Example usage
    runner = SimulationRunner()
    
    # Test on small graph
    result = runner.run_single_experiment(
        n=10, k=2, p=0.5, algorithm_name='FirstFit', algorithm_func=None, seed=42
    )
    print(f"Test result: {result}")

