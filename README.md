# COMP 6651 Project: Online Graph Coloring Algorithms

This project implements and evaluates greedy algorithms for online graph coloring, specifically the FirstFit and CBIP (Coloring Based on Interval Partitioning) algorithms.

## Project Structure

```
ADT_PROJECT/
├── graph_generator.py      # Random k-colourable graph generator
├── coloring_algorithms.py  # FirstFit, CBIP, and FirstFitHeuristic implementations
├── simulation.py           # Simulation framework and metrics calculation
├── results_table.py        # Results table generation (CSV, Markdown, LaTeX)
├── main.py                 # Main script to run all experiments
├── README.md               # This file
└── graphs/                 # Directory for generated graphs (created automatically)
```

## Requirements

- Python 3.7 or higher
- Standard library only (no external dependencies)

## Installation

No installation required. Just ensure you have Python 3.7+ installed.

## Usage

### Quick Start

Run all simulations with default parameters:

```bash
python main.py
```

This will:
1. Generate random k-colourable graphs for all configurations
2. Run FirstFit algorithm for k ∈ {2, 3, 4}
3. Run CBIP algorithm for k = 2
4. Run FirstFitHeuristic for k ∈ {2, 3, 4}
5. Generate results tables in CSV, Markdown, and LaTeX formats

### Configuration

Edit `main.py` to change parameters:

```python
n_values = [50, 100, 200, 400, 800, 1600]  # Vertex counts
k_values_firstfit = [2, 3, 4]              # Chromatic numbers for FirstFit
k_values_cbip = [2]                        # Chromatic numbers for CBIP
p = 0.5                                    # Edge probability
N = 100                                    # Number of graphs per configuration
seed = 42                                  # Random seed
```

### Individual Components

#### Generate Graphs Only

```python
from graph_generator import generate_multiple_graphs

generate_multiple_graphs(n=100, k=2, p=0.5, N=100, output_dir="graphs")
```

#### Run Single Experiment

```python
from simulation import SimulationRunner

runner = SimulationRunner()
result = runner.run_single_experiment(
    n=100, k=2, p=0.5, algorithm_name='FirstFit', 
    algorithm_func=None, seed=42
)
print(result)
```

#### Run Batch Experiments

```python
from simulation import SimulationRunner

runner = SimulationRunner()
results = runner.run_batch_experiments(
    n=100, k=2, p=0.5, N=100, 
    algorithm_name='FirstFit', seed=42
)
print(f"Average competitive ratio: {results['avg_competitive_ratio']:.4f}")
```

## Algorithms

### FirstFit
Upon arrival of a vertex, colors it with the smallest natural number that hasn't been used by its existing neighbors.

### CBIP (Coloring Based on Interval Partitioning)
For a k-colourable graph:
1. Computes a k-partition of current vertices into k independent sets
2. Finds which set the new vertex belongs to
3. Colors the vertex with the smallest number not used by vertices outside its set

### FirstFitHeuristic
A heuristic improvement of FirstFit that orders vertices by degree (non-increasing) before coloring.

## Output Files

After running `main.py`, you'll get:

- `results_table.csv` - Results in CSV format
- `results_table.md` - Results in Markdown table format
- `results_table.tex` - Results in LaTeX table format
- `graphs/` - Directory containing all generated graphs in EDGES format

## Graph Format (EDGES)

Graphs are stored in ASCII EDGES format:

```
# Online k-colourable graph
# n=100, k=2, p=0.50
# Vertex ordering: 5 12 3 8 ...
# EDGES format
100 250
1 2
1 5
2 3
...
```

## Metrics

The simulation calculates:

- **Competitive Ratio**: ρ(Alg, G) = (number of colors used) / χ(G)
- **Average Competitive Ratio**: Mean over N graphs
- **Standard Deviation**: SD of competitive ratios over N graphs

## Testing

To test the implementation on a small example:

```python
from graph_generator import GraphGenerator
from coloring_algorithms import FirstFit, CBIP

# Generate small graph
gen = GraphGenerator(n=10, k=2, p=0.5, seed=42)
gen.generate()
ordering = gen.get_online_ordering()

# Test FirstFit
firstfit = FirstFit()
def get_neighbors(v, revealed):
    return gen.get_edges_for_vertex(v, revealed)
coloring = firstfit.color_online_graph(ordering, get_neighbors)
print(f"FirstFit used {firstfit.get_num_colors()} colors")

# Test CBIP
cbip = CBIP(k=2)
coloring = cbip.color_online_graph(ordering, get_neighbors)
print(f"CBIP used {cbip.get_num_colors()} colors")
```

## Project Deliverables

1. **Implementation Code**: All Python files in this repository
2. **Generated Graphs**: All graphs in EDGES format (in `graphs/` directory)
3. **Results Tables**: Generated tables with simulation results
4. **README**: This file

## Notes

- The implementation uses only Python standard library (no external dependencies)
- Graphs are generated following the pseudocode from the project specification
- All algorithms are implemented from scratch
- The heuristic (FirstFitHeuristic) uses degree-based ordering

## Team Information

[Add your team members and student numbers here]

## References

[1] Y. Li, V. Narayan, and D. Pankratov, "Online coloring and a new type of adversary for online graph problems," Algorithmica, vol. 84, pp. 1232-1251, 2022.

[2] A. Gyárfás and J. Lehel, "On-line and first fit colorings of graphs," Journal of Graph Theory, vol. 12, no. 2, pp. 217-227, 1988.

[3] L. Lovász, M. Saks, and W. Trotter, "An on-line graph coloring algorithm with sublinear performance ratio," in Graph Theory and combinatorics 1988 (B. Bollobás, ed.), vol. 43 of Annals of Discrete Mathematics, pp. 319-325, Elsevier, 1989.

# ADTProject
