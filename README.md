# 📚 COMP 6651 Project: Online Graph Coloring Algorithms

This project implements and evaluates greedy algorithms for online graph coloring, specifically the **FirstFit**, **CBIP (Coloring Based on Interval Partitioning)**, and a **FirstFitHeuristic** algorithm. The implementation strictly adheres to the project constraint of using **only Python's standard library**.

---

## 🏗️ Project Structure

The repository is organized as follows:

```text
ADT_PROJECT/
├── graph_generator.py          # Random k-colourable graph generator (GENERATE ONLINE KCOLOURABLE GRAPH)
├── coloring_algorithms.py      # FirstFit, CBIP, and FirstFitHeuristic implementations
├── simulation_runner.py        # Simulation framework and metrics calculation
├── results_table.py            # Results table generation (CSV, Markdown, LaTeX)
├── analysis.py                 # Function fitting and trend analysis
├── csv_generation.py           # Batch experiment execution using predefined parameters
├── main.py                     # Interactive simulation interface
├── README.md                   # This file
├── graphs/                     # Directory to store generated graphs in EDGES format
└── user_graphs/                # Directory for user-defined graphs

## ⚙️ Requirements

* **Python 3.7** or higher
* No external libraries (Standard library only).

---

## 🚀 Quick Start

### Interactive Mode (Recommended for Beginners)

Use the interactive script to run single simulations, test parameters, and view results in real-time.

```bash
python main.py

### Batch Mode (For Full Benchmark)

Run the complete empirical study with predefined parameters (as specified in Table 1 of the project specs) to generate all required output tables and analysis files.

```bash
python csv_generation.py

## Usage Examples

### 1. Interactive Single Simulation

Run the interactive mode:

```bash
python main.py