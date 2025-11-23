# Project Implementation Summary

This document provides an overview of the COMP 6651 project implementation.

## Files Created

### Core Implementation Files

1. **`graph_generator.py`**
   - Implements random k-colourable graph generation
   - Follows the pseudocode from the project specification
   - Supports saving/loading graphs in EDGES format
   - Generates online vertex orderings

2. **`coloring_algorithms.py`**
   - **FirstFit**: Basic greedy algorithm that colors vertices with smallest available color
   - **CBIP**: Coloring Based on Interval Partitioning algorithm for k-colourable graphs
   - **FirstFitHeuristic**: Improved FirstFit using degree-based vertex ordering

3. **`simulation.py`**
   - Simulation framework for running experiments
   - Calculates competitive ratio, average competitive ratio, and standard deviation
   - Supports batch experiments and full simulation runs

4. **`results_table.py`**
   - Generates results tables in multiple formats:
     - CSV format
     - Markdown format
     - LaTeX format

5. **`main.py`**
   - Main script to run all experiments
   - Generates graphs, runs all algorithms, and produces results tables

### Testing and Documentation

6. **`test_example.py`**
   - Test script to verify implementation correctness
   - Tests all three algorithms on a small example graph

7. **`README.md`**
   - Complete documentation with usage instructions
   - Installation and configuration guide

## How to Run

### Quick Start
```bash
python main.py
```

This will:
1. Generate all required graphs
2. Run FirstFit for k ∈ {2, 3, 4}
3. Run CBIP for k = 2
4. Run FirstFitHeuristic for k ∈ {2, 3, 4}
5. Generate results tables

### Test Implementation
```bash
python test_example.py
```

## Key Features

### Graph Generation
- Generates random k-colourable graphs following project specification
- Ensures at least one edge between each vertex and each other independent set
- Adds additional edges with probability p
- Saves graphs in EDGES format with vertex ordering

### Algorithms

**FirstFit**: 
- Colors each vertex with smallest available color
- Simple and efficient

**CBIP**:
- Computes k-partition of current graph
- Colors vertex based on colors used outside its partition set
- Designed for k-colourable graphs

**FirstFitHeuristic**:
- Orders vertices by degree (non-increasing) before coloring
- Often improves performance over basic FirstFit

### Metrics
- Competitive ratio: ρ(Alg, G) = (colors used) / χ(G)
- Average competitive ratio over N graphs
- Standard deviation of competitive ratios

## Output

After running `main.py`, you'll get:
- `results_table.csv` - Results in CSV format
- `results_table.md` - Results in Markdown table format  
- `results_table.tex` - Results in LaTeX table format
- `graphs/` - Directory with all generated graphs in EDGES format

## Configuration

Edit `main.py` to change:
- `n_values`: List of vertex counts to test
- `k_values_firstfit`: Chromatic numbers for FirstFit
- `k_values_cbip`: Chromatic numbers for CBIP
- `p`: Edge probability
- `N`: Number of graphs per configuration
- `seed`: Random seed for reproducibility

## Implementation Notes

1. **No External Dependencies**: Uses only Python standard library
2. **Proper Colorings**: All algorithms ensure no adjacent vertices have the same color
3. **Reproducibility**: Uses random seeds for consistent results
4. **Efficiency**: Optimized for large-scale simulations

## Next Steps

1. Run `python main.py` to generate all results
2. Review the generated tables
3. Analyze the results for your report
4. Consider additional heuristics or parameter variations

## For Your Report

You'll need to:
1. Document your implementation details
2. Explain your testing methodology
3. Present and analyze the results tables
4. Discuss the heuristic choice (degree-based ordering)
5. Explain why CBIP is only tested on k=2 (computational complexity)

## Questions to Address in Report

1. **Why CBIP only for k=2?**
   - For k=2, computing a 2-partition is polynomial (bipartite graph)
   - For k≥3, finding a k-partition is NP-hard in general
   - Even though graphs are k-colourable, finding the partition is computationally expensive

2. **Heuristic Choice**
   - Degree-based ordering: vertices with higher degree are colored first
   - Rationale: High-degree vertices are more constrained, so coloring them early can prevent conflicts

3. **Results Analysis**
   - Compare competitive ratios across different n and k values
   - Analyze how performance scales with graph size
   - Compare FirstFit vs FirstFitHeuristic

