# 📚 COMP 6651 Project: Online Graph Coloring Algorithms


**Department of Computer Science and Software Engineering**  
**Concordia University**  
**Algorithm Design Techniques - Fall 2025**


This project implements and evaluates greedy algorithms for online graph coloring, specifically the **FirstFit**, **CBIP (Coloring Based on Interval Partitioning)**, and a **FirstFitHeuristic** algorithm. The implementation strictly adheres to the project constraint of using **only Python's standard library**.


---


## 🎯 Project Overview


### What is Online Graph Coloring?


An **online graph** reveals its vertices and edges incrementally - at each time step, one vertex together with its edges to existing vertices is revealed. The **online graph coloring problem** requires assigning a proper color to each vertex as it arrives (no two adjacent vertices can have the same color), with the constraint that once assigned, colors cannot be changed.


### Algorithms Implemented


1. **FirstFit Algorithm**: Colors each vertex with the smallest available color not used by its revealed neighbors
2. **CBIP Algorithm**: For k-colorable graphs, partitions the current graph into k independent sets and colors strategically
3. **FirstFitHeuristic**: Enhanced FirstFit using minimum-degree-first ordering in the revealed subgraph


---


## 🏗️ Project Structure


```text
ADTProject/
├── graph_generator.py          # Random k-colorable graph generator
├── coloring_algorithms.py      # FirstFit, CBIP, and FirstFitHeuristic implementations
├── simulation_runner.py        # Simulation framework and metrics calculation
├── results_table.py            # Results table generation (CSV, Markdown, LaTeX)
├── analysis.py                 # Function fitting and trend analysis
├── csv_generation.py           # Batch experiment execution
├── main.py                     # Interactive simulation interface
├── README.md                   # This file
├── graphs/                     # Directory for generated benchmark graphs
└── user_graphs/                # Directory for interactive session graphs
```


---


## ⚙️ Requirements


- **Python 3.7** or higher
- **No external libraries** (Standard library only)


---
## 🎮 Usage Examples


### 1. Interactive Single Simulation


```bash
python main.py
```


Choose algorithm → Set parameters → View results


### 2. Comparative Study


```bash
python main.py
# Select option 3 for "Run All Algorithms"
```


### 3. Full Benchmark (Table 1 Recreation)


```bash
python csv_generation.py
```


Generates complete results matching project specifications.


### 4. Custom Analysis


```python
from analysis import FunctionFittingAnalysis
analyzer = FunctionFittingAnalysis()
analyzer.analyze_results("results_table.csv")
```


---

## 🚀 Quick Start


### Interactive Mode (Recommended for Testing)


Run single simulations with custom parameters:


```bash
python main.py
```


**Features:**
- Choose algorithm (FirstFit, CBIP, FirstFitHeuristic, or comparative study)
- Set custom parameters (n, k, p, number of instances)
- View real-time results and competitive ratios
- Inspect ASCII graph encodings


### Batch Mode (Full Benchmark Study)


Execute the complete empirical study with predefined parameters:


```bash
python csv_generation.py
```


**Generates:**
- Complete benchmark results for all algorithms
- CSV, Markdown, and LaTeX result tables
- Analysis files for trend fitting


---


## 📊 Experimental Design


### Parameters


| Parameter | Description | Values |
|-----------|-------------|---------|
| **n** | Number of vertices | 50, 100, 200, 400, 800, 1600 |
| **k** | Chromatic number | 2, 3, 4 (FirstFit/Heuristic), 2 (CBIP) |
| **p** | Edge probability | 0.5 |
| **N** | Graphs per configuration | 100 |


### Metrics


- **Competitive Ratio**: `ρ(Alg, G) = colors_used_by_Alg / χ(G)`
- **Average Competitive Ratio**: Mean over N graph instances
- **Standard Deviation**: Measure of performance consistency


---


## 🔬 Algorithm Details


### FirstFit Algorithm
```
Upon vertex v arrival:
1. Find neighbors of v in revealed graph
2. Collect colors used by neighbors
3. Assign smallest unused color to v
```


### CBIP Algorithm (k=2 only)
```
Upon vertex v arrival:
1. Find connected component CC of v in revealed graph
2. Bipartition CC into sets A and B (v ∈ A)
3. Color v with smallest color not used in B
```


### FirstFitHeuristic Algorithm
```
Enhancement: Select next vertex with minimum degree in revealed subgraph
1. Among unrevealed vertices, choose one with fewest revealed neighbors
2. Apply FirstFit coloring to selected vertex
```


---


## 📁 File Formats


### EDGES Format
Graphs are stored in ASCII-readable EDGES format:
```
# Vertex ordering: 3 1 4 2 5
1 2
1 3
2 4
3 4
4 5
```


**Benefits:**
- Human-readable
- Reproducible experiments
- Standard format
- Compact representation


---



## 📈 Expected Results


### Competitive Ratios (Theoretical)
- **FirstFit**: O(log n) for general graphs
- **CBIP (k=2)**: Optimal ratio of 2 for bipartite graphs
- **FirstFitHeuristic**: Improved performance over standard FirstFit


### Why CBIP Limited to k=2?
For k ≥ 3, finding optimal k-partitions becomes computationally intractable (NP-hard), making empirical studies impractical for large graphs.


---


## 🔧 Implementation Notes


### Graph Generation Algorithm
```python
def generate_k_colorable_graph(n, k, p):
    # 1. Partition vertices into k independent sets
    # 2. Ensure at least one edge between each pair of sets
    # 3. Add additional edges with probability p
    # 4. Randomize vertex ordering for online presentation
```


### Key Design Decisions
- **Modular architecture**: Separate concerns (generation, algorithms, simulation)
- **Reproducible randomness**: Seeded random number generation
- **Efficient data structures**: Sets and dictionaries for O(1) lookups
- **Memory optimization**: Process graphs individually to handle large datasets


---


## 📋 Project Deliverables


✅ **Random k-colorable graph generator**  
✅ **FirstFit algorithm implementation**  
✅ **CBIP algorithm implementation (k=2)**  
✅ **FirstFitHeuristic algorithm implementation**  
✅ **Empirical study framework**  
✅ **Results tables (CSV, Markdown, LaTeX)**  
✅ **Interactive simulation interface**  
✅ **Function fitting and trend analysis**  


---


## 🚨 Important Notes


### Computational Complexity
- **FirstFit**: O(n²) per graph
- **CBIP**: O(n³) per graph (bipartition computation)
- **FirstFitHeuristic**: O(n²) per graph


### Memory Requirements
- Graphs stored individually to handle large datasets
- Peak memory usage: O(n²) for adjacency information


### Reproducibility
- All experiments use seeded random generation
- Graph files can be regenerated with identical results
- Results tables include all parameters for replication


---


## 🎯 Academic Context


This project demonstrates:
- **Online algorithm analysis** and competitive ratio evaluation
- **Greedy algorithm design** and performance comparison
- **Empirical algorithm study** methodology
- **Graph theory applications** in computer science
- **Algorithm engineering** principles


---


**Course**: COMP 6651 Algorithm Design Techniques  
**Institution**: Concordia University  
**Semester**: Fall 2025
**Team Members**: Sahiti Chilakala(40304091), Anosh kurian Vadakkeparampil(40303184), Rolwyn Raju(40303902) ,Pretty Pramod Kotian(40320857)
