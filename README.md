COMP 6651 Project: Online Graph Coloring Algorithms
This project implements and evaluates greedy algorithms for online graph coloring, specifically the FirstFit, CBIP (Coloring Based on Interval Partitioning), and FirstFitHeuristic algorithms.

Project Structure
text
ADT_PROJECT/
├── graph_generator.py          # Random k-colourable graph generator
├── coloring_algorithms.py      # FirstFit, CBIP, and FirstFitHeuristic implementations  
├── simulation_runner.py        # Simulation framework and metrics calculation
├── results_table.py            # Results table generation (CSV, Markdown, LaTeX)
├── analysis.py                 # Function fitting and trend analysis
├── csv_generation.py           # Batch experiment execution
├── main.py                     # Interactive simulation interface
├── README.md                   # This file
├── graphs/                     # Generated graphs (created automatically)
└── user_graphs/                # User-generated graphs (created automatically)
Requirements
Python 3.7 or higher

Standard library only (no external dependencies)

Installation
No installation required. Just ensure you have Python 3.7+ installed.

Quick Start
Interactive Mode (Recommended for Beginners)
python main.py
This launches an interactive menu where you can:

Choose algorithms (FirstFit, CBIP, FirstFitHeuristic)

Set custom parameters (vertices, chromatic number, edge probability)

View real-time results and ASCII encoding information

Run comparative studies

Batch Mode (For Full Benchmark)

python csv_generation.py
This runs the complete benchmark study with predefined parameters and generates comprehensive results.

Usage Examples
1. Interactive Single Simulation
python main.py
Then choose:

Algorithm: 0 (FirstFit), 1 (CBIP), 2 (FirstFitHeuristic), or 3 (All algorithms)

Vertices (n): 100

Graph instances: 10

Edge probability: 0.5

Chromatic number: 3 (for FirstFit/Heuristic)

2. Complete Benchmark Study

python csv_generation.py
Runs comprehensive experiments with:

Vertex counts: [50, 100, 200, 400, 800, 1600]

Chromatic numbers: 2, 3, 4

100 graphs per configuration

All three algorithms

3. Advanced Analysis

python analysis.py
Performs function fitting and trend analysis on existing results.

Configuration
Main Parameters in csv_generation.py:

n_values = [50, 100, 200, 400, 800, 1600]  # Vertex counts
k_values_firstfit = [2, 3, 4]              # Chromatic numbers for FirstFit
k_values_cbip = [2]                        # Chromatic numbers for CBIP  
p = 0.5                                    # Edge probability
N = 100                                    # Number of graphs per configuration
seed = 42                                  # Random seed
Algorithms
FirstFit
Description: Colors each vertex with the smallest available color not used by its neighbors

Complexity: O(n²) in worst case

Theoretical Bound: O(n) competitive ratio for general graphs

CBIP (Coloring Based on Interval Partitioning)
Description: Partitions graph into bipartite sets and colors optimally within partitions

Complexity: O(n²)

Theoretical Bound: Optimal for bipartite graphs (competitive ratio = 1)

FirstFitHeuristic
Description: FirstFit with vertex ordering by degree (lowest degree first)

Complexity: O(n²)

Advantage: Often outperforms standard FirstFit in practice

Output Files
After execution, you'll get:

Results Files:
results_table.csv - Raw results in CSV format

results_table.md - Formatted Markdown table

results_table.tex - LaTeX table for papers

function_fitting_analysis.txt - Detailed trend analysis

Graph Files (in graphs/ directory):
ASCII EDGES format with vertex ordering

Human-readable format for reproducibility

Example: graph_n100_k2_p0.50_run1.edges

Graph Format Specification
Graphs use EDGES ASCII encoding:

text
# Vertex ordering: 3 1 4 2 5
1 2
1 3  
2 4
3 4
4 5
Format Details:

Comment lines start with #

Vertex ordering stored in header comment

Each edge represented as two space-separated integers

Undirected edges (symmetric)

Human-readable and machine-parsable

Key Metrics
Competitive Ratio
text
ρ(Algorithm, Graph) = (Colors Used) / (Chromatic Number)
Evaluation Metrics:
Average Competitive Ratio: Mean over N graph instances

Standard Deviation: Variability across instances

Function Fitting: Identifies growth patterns (constant, linear, logarithmic)

Trend Analysis: Performance scaling with graph size

Example Results
Algorithm	k	n	Avg Ratio	Std Dev
FirstFit	2	100	1.85	0.12
CBIP	2	100	1.00	0.00
FirstFitHeuristic	3	200	2.45	0.15
Testing & Validation
Quick Test:
python
from graph_generator import GraphGenerator
from coloring_algorithms import FirstFit, CBIP

# Generate test graph
gen = GraphGenerator(n=10, k=2, p=0.5, seed=42)
ordering = gen.get_online_ordering()

# Test algorithms
firstfit = FirstFit()
coloring_ff = firstfit.color_online_graph(ordering, gen.get_edges_for_vertex)
print(f"FirstFit colors: {firstfit.get_num_colors()}")

cbip = CBIP()  
coloring_cbip = cbip.color_online_graph(ordering, gen.get_edges_for_vertex)
print(f"CBIP colors: {cbip.get_num_colors()}")
Project Features
✅ Complete Implementation: All algorithms from scratch
✅ ASCII Graph Encoding: Human-readable format
✅ Comprehensive Analysis: Function fitting and trends
✅ Interactive Interface: User-friendly menu system
✅ Batch Processing: Parallel graph generation
✅ Multiple Output Formats: CSV, Markdown, LaTeX
✅ Theoretical Validation: Confirms known bounds
✅ Scalability Testing: Up to 1600 vertices

Performance Notes
Memory Efficient: Uses adjacency lists and streaming

Time Optimized: Multiprocessing for graph generation

Cache Friendly: Adjacency dict caching for repeated access

Progress Tracking: tqdm progress bars for long runs

Team Information
Team members and student numbers would be added here

References
[1] Y. Li, V. Narayan, and D. Pankratov, "Online coloring and a new type of adversary for online graph problems," Algorithmica, vol. 84, pp. 1232-1251, 2022.

[2] A. Gyárfás and J. Lehel, "On-line and first fit colorings of graphs," Journal of Graph Theory, vol. 12, no. 2, pp. 217-227, 1988.

[3] L. Lovász, M. Saks, and W. Trotter, "An on-line graph coloring algorithm with sublinear performance ratio," in Graph Theory and combinatorics 1988 (B. Bollobás, ed.), vol. 43 of Annals of Discrete Mathematics, pp. 319-325, Elsevier, 1989.

License
This project is for academic purposes as part of COMP 6651 coursework.