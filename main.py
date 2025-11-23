"""
Main script to run all simulations for the COMP 6651 project.

This script:
1. Generates random k-colourable graphs
2. Runs FirstFit algorithm for k in {2, 3, 4}
3. Runs CBIP algorithm for k = 2
4. Runs FirstFitHeuristic for k in {2, 3, 4}
5. Generates results tables
"""

import os
from simulation import SimulationRunner, generate_all_graphs
from results_table import generate_results_table, generate_markdown_table, generate_latex_table


def main():
    """Main execution function."""
    
    # Configuration parameters
    n_values = [50, 100, 200, 400, 800, 1600]  # Vertex counts
    k_values_firstfit = [2, 3, 4]  # Chromatic numbers for FirstFit
    k_values_cbip = [2]  # Chromatic numbers for CBIP
    p = 0.5  # Edge probability
    N = 100  # Number of graphs per configuration
    seed = 42  # Random seed for reproducibility
    graph_dir = "graphs"
    
    print("=" * 60)
    print("COMP 6651 Project: Online Graph Coloring")
    print("=" * 60)
    print(f"Parameters: p={p}, N={N}, seed={seed}")
    print()
    
    # Create output directory
    os.makedirs(graph_dir, exist_ok=True)
    
    # Step 1: Generate all graphs
    print("Step 1: Generating graphs...")
    print("-" * 60)
    all_k_values = list(set(k_values_firstfit + k_values_cbip))
    generate_all_graphs(n_values, all_k_values, p, N, graph_dir, seed)
    print()
    
    # Step 2: Run FirstFit experiments
    print("Step 2: Running FirstFit experiments...")
    print("-" * 60)
    runner = SimulationRunner()
    firstfit_results = runner.run_full_simulation(
        n_values, k_values_firstfit, p, N, 'FirstFit', graph_dir, seed
    )
    print()
    
    # Step 3: Run CBIP experiments
    print("Step 3: Running CBIP experiments...")
    print("-" * 60)
    cbip_results = runner.run_full_simulation(
        n_values, k_values_cbip, p, N, 'CBIP', graph_dir, seed
    )
    print()
    
    # Step 4: Run FirstFitHeuristic experiments
    print("Step 4: Running FirstFitHeuristic experiments...")
    print("-" * 60)
    heuristic_results = runner.run_full_simulation(
        n_values, k_values_firstfit, p, N, 'FirstFitHeuristic', graph_dir, seed
    )
    print()
    
    # Step 5: Generate results tables
    print("Step 5: Generating results tables...")
    print("-" * 60)
    all_results = firstfit_results + cbip_results + heuristic_results
    
    # Sort results for consistent table ordering
    all_results.sort(key=lambda x: (x['algorithm'], x['k'], x['n']))
    
    generate_results_table(all_results, "results_table.csv")
    generate_markdown_table(all_results, "results_table.md")
    generate_latex_table(all_results, "results_table.tex")
    
    print()
    print("=" * 60)
    print("Simulation complete!")
    print("=" * 60)
    print(f"Results saved to:")
    print(f"  - results_table.csv")
    print(f"  - results_table.md")
    print(f"  - results_table.tex")
    print(f"Graphs saved to: {graph_dir}/")


if __name__ == "__main__":
    main()

