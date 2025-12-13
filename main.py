import os
import sys
from typing import List, Set, Tuple, Dict
from graph_generator import GraphGenerator
from coloring_algorithms import FirstFit, CBIP, FirstFitHeuristic
from simulation_runner import SimulationRunner


class InteractiveSimulation:
    def __init__(self):
        self.runner = SimulationRunner()
        self.graphs_dir = "user_graphs"
        os.makedirs(self.graphs_dir, exist_ok=True)
    
    def display_menu(self):
        """Display the main menu."""
        print("\n" + "="*60)
        print("ONLINE GRAPH COLORING SIMULATION")
        print("="*60)
        print("Choose algorithm:")
        print("  0 - FirstFit Algorithm")
        print("  1 - CBIP Algorithm (k=2 only)")
        print("  2 - FirstFitHeuristic Algorithm")
        print("  3 - Run All Algorithms (Comparative Study)")
        print("  4 - Exit")
        print("-"*60)
    
    def get_user_input(self) -> Dict:
        params = {}
        
        while True:
            try:
                choice = input("Enter your choice (0-4): ").strip()
                if choice in ['0', '1', '2', '3', '4']:
                    params['algorithm_choice'] = int(choice)
                    break
                else:
                    print("Invalid choice. Please enter 0, 1, 2, 3, or 4.")
            except ValueError:
                print("Please enter a valid number.")
        
        if params['algorithm_choice'] == 4:
            return params
        while True:
            try:
                n = int(input("Enter number of vertices (n): "))
                if n > 0:
                    params['n'] = n
                    break
                else:
                    print("Number of vertices must be positive.")
            except ValueError:
                print("Please enter a valid integer.")
        
        while True:
            try:
                N = int(input("Enter number of graph instances to generate: "))
                if N > 0:
                    params['N'] = N
                    break
                else:
                    print("Number of instances must be positive.")
            except ValueError:
                print("Please enter a valid integer.")
        
        while True:
            try:
                p = float(input("Enter edge probability (0.0 - 1.0): "))
                if 0.0 <= p <= 1.0:
                    params['p'] = p
                    break
                else:
                    print("Probability must be between 0.0 and 1.0.")
            except ValueError:
                print("Please enter a valid number.")
        if params['algorithm_choice'] in [0, 2, 3]:
            while True:
                try:
                    k = int(input("Enter chromatic number (k): "))
                    if k >= 2:
                        params['k'] = k
                        break
                    else:
                        print("Chromatic number must be at least 2.")
                except ValueError:
                    print("Please enter a valid integer.")
        else:
            params['k'] = 2
            print("CBIP algorithm selected - using k=2 (bipartite graphs)")
        
        return params
    
    def run_single_simulation(self, params: Dict):
        print(f"\nRunning simulation with parameters:")
        print(f"  Vertices (n): {params['n']}")
        print(f"  Chromatic number (k): {params['k']}")
        print(f"  Graph instances: {params['N']}")
        print(f"  Edge probability: {params['p']}")
        print(f"\nGenerating {params['N']} graph instances...")
        graph_files = []
        for i in range(params['N']):
            filename = os.path.join(self.graphs_dir, f"user_graph_{params['n']}_{params['k']}_{i+1}.edges")
            graph_files.append(filename)
            gen = GraphGenerator(params['n'], params['k'], params['p'], seed=42 + i)
            ordering = gen.get_online_ordering()
            gen.save_to_edges_format(filename, ordering)
            if i == 0:
                print(f"\nSample ASCII Encoding (Graph 1):")
                print(f"  File: {filename}")
                print(f"  Format: EDGES format with vertex ordering")
                print(f"  Vertex ordering: {ordering[:10]}{'...' if len(ordering) > 10 else ''}")
                print(f"  Edge count: {len(gen.edges)}")

        algorithms = []
        if params['algorithm_choice'] == 0:
            algorithms = ['FirstFit']
        elif params['algorithm_choice'] == 1:
            algorithms = ['CBIP']
        elif params['algorithm_choice'] == 2:
            algorithms = ['FirstFitHeuristic']
        elif params['algorithm_choice'] == 3:
            algorithms = ['FirstFit', 'CBIP', 'FirstFitHeuristic']
        results = []
        for algorithm in algorithms:
            print(f"\nRunning {algorithm} algorithm...")
            current_k = params['k'] if algorithm != 'CBIP' else 2
            
            batch_result = self.runner.run_batch_experiments(
                n=params['n'],
                k=current_k,
                p=params['p'],
                N=params['N'],
                algorithm_name=algorithm,
                graph_files=graph_files,
                seed=42
            )
            results.append(batch_result)
            
            print(f"  Average competitive ratio: {batch_result['avg_competitive_ratio']:.4f}")
            print(f"  Standard deviation: {batch_result['std_dev']:.4f}")
        
        self.display_results(results, params)
        
        return results
    
    def display_results(self, results: List[Dict], params: Dict):
        print("\n" + "="*60)
        print("SIMULATION RESULTS")
        print("="*60)
        
        for result in results:
            print(f"\nAlgorithm: {result['algorithm']}")
            print(f"  Competitive Ratio: {result['avg_competitive_ratio']:.4f} ± {result['std_dev']:.4f}")
            print(f"  Graph Size: n={result['n']}, k={result['k']}")
            print(f"  Samples: {result['N']} graphs")
            
    
    def run_benchmark_study(self):
        print("\n" + "="*60)
        print("RUNNING PROJECT BENCHMARK STUDY")
        print("="*60)
        n_values = [50, 100, 200, 400, 800, 1600]
        k_values_firstfit = [2, 3, 4]
        k_values_cbip = [2]
        p = 0.5
        N = 100
        seed = 42
        graph_dir = "benchmark_graphs"
        
        print("Parameters:")
        print(f"  Vertex counts: {n_values}")
        print(f"  Chromatic numbers: {k_values_firstfit} (FirstFit), {k_values_cbip} (CBIP)")
        print(f"  Edge probability: {p}")
        print(f"  Graphs per configuration: {N}")
        print(f"  Total graphs: {len(n_values) * (len(k_values_firstfit) + len(k_values_cbip)) * N}")
        
        print(f"\nGenerating benchmark graphs...")
        all_k_values = list(set(k_values_firstfit + k_values_cbip))
        self.runner.generate_all_graphs(n_values, all_k_values, p, N, graph_dir, seed)
        
        print(f"\nRunning FirstFit experiments...")
        firstfit_results = self.runner.run_full_simulation(
            n_values, k_values_firstfit, p, N, 'FirstFit', graph_dir, seed
        )
        
        print(f"\nRunning CBIP experiments...")
        cbip_results = self.runner.run_full_simulation(
            n_values, k_values_cbip, p, N, 'CBIP', graph_dir, seed
        )
        
        print(f"\nRunning FirstFitHeuristic experiments...")
        heuristic_results = self.runner.run_full_simulation(
            n_values, k_values_firstfit, p, N, 'FirstFitHeuristic', graph_dir, seed
        )
        
        all_results = firstfit_results + cbip_results + heuristic_results
        all_results.sort(key=lambda x: (x['algorithm'], x['k'], x['n']))
        
        print("\n" + "="*60)
        print("BENCHMARK STUDY SUMMARY")
        print("="*60)
        
        for result in all_results:
            print(f"{result['algorithm']:15} k={result['k']} n={result['n']:4} : {result['avg_competitive_ratio']:.4f}")
        
        print(f"\nResults saved to: {graph_dir}/")
        print("Use analysis.py for detailed function fitting and trend analysis.")
        
        return all_results
    
    def display_ascii_encoding_info(self):
        """Display information about ASCII graph encodings."""
        print("\n" + "="*60)
        print("ASCII GRAPH ENCODING INFORMATION")
        print("="*60)
        print("""
The graphs are stored in EDGES format, which is an ASCII-readable format.

Format Specification:
- Each line represents an undirected edge as two vertex numbers
- Example: "1 2" represents an edge between vertex 1 and vertex 2
- Vertex ordering is stored in a comment line
- Files are human-readable and can be inspected with any text editor

Example file content:
  # Vertex ordering: 3 1 4 2 5
  1 2
  1 3
  2 4
  3 4
  4 5

This encoding ensures:
1. Reproducibility - same graph can be reloaded
2. Transparency - graph structure is visible
3. Standardization - follows established format
4. Efficiency - compact representation

Graphs are generated using the project specification algorithm:
1. Vertices are assigned to k independent sets
2. Edges are added between sets with probability p
3. At least one edge is guaranteed between each pair of sets
        """)
    
    def main_loop(self):
        """Main interactive loop."""
        print("Welcome to Online Graph Coloring Simulation")
        print("This tool implements FirstFit and CBIP algorithms for online graph coloring")
        
        while True:
            self.display_menu()
            params = self.get_user_input()
            
            if params['algorithm_choice'] == 4:
                print("Thank you for using the Online Graph Coloring Simulation!")
                break
            
            elif params['algorithm_choice'] == 5:  
                self.run_benchmark_study()
            
            elif 'algorithm_choice' in params:
                try:
                    self.run_single_simulation(params)
                    
                    show_info = input("\nShow ASCII encoding information? (y/n): ").strip().lower()
                    if show_info == 'y':
                        self.display_ascii_encoding_info()
                    
                    continue_sim = input("\nRun another simulation? (y/n): ").strip().lower()
                    if continue_sim != 'y':
                        print("Thank you for using the Online Graph Coloring Simulation!")
                        break
                        
                except Exception as e:
                    print(f"Error during simulation: {e}")
                    print("Please check your parameters and try again.")
            
            else:
                print("Invalid parameters. Please try again.")


def main():
    """Main entry point."""
    try:
        simulator = InteractiveSimulation()
        simulator.main_loop()
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()