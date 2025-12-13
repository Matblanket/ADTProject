import os
from simulation_runner import SimulationRunner
from results_table import generate_results_table, generate_markdown_table, generate_latex_table
from analysis import FunctionFittingAnalysis


class CsvGeneration:
    def __init__(self):
        self.n_values = [50, 100, 200, 400, 800, 1600]
        self.k_values_firstfit = [2, 3, 4]
        self.k_values_cbip = [2]
        self.p = 0.5
        self.N = 100
        self.seed = 42
        self.graph_dir = "graphs"
        self.runner = SimulationRunner()
        self.analyzer = FunctionFittingAnalysis()

        os.makedirs(self.graph_dir, exist_ok=True)

    def run(self):
        print("=" * 60)
        print("COMP 6651 Project: Online Graph Coloring")
        print("=" * 60)
        print(f"Parameters: p={self.p}, N={self.N}, seed={self.seed}")
        print()

        print("Step 1: Generating graphs...")
        all_k_values = list(set(self.k_values_firstfit + self.k_values_cbip))
        self.runner.generate_all_graphs(
            self.n_values,
            all_k_values,
            self.p,
            self.N,
            self.graph_dir,
            self.seed
        )
        print()

        print("Step 2: Running FirstFit experiments...")
        firstfit_results = self.runner.run_full_simulation(
            self.n_values,
            self.k_values_firstfit,
            self.p,
            self.N,
            'FirstFit',
            self.graph_dir,
            self.seed
        )
        print()

        print("Step 3: Running CBIP experiments...")
        cbip_results = self.runner.run_full_simulation(
            self.n_values,
            self.k_values_cbip,
            self.p,
            self.N,
            'CBIP',
            self.graph_dir,
            self.seed
        )
        print()

        print("Step 4: Running FirstFitHeuristic experiments...")
        heuristic_results = self.runner.run_full_simulation(
            self.n_values,
            self.k_values_firstfit,
            self.p,
            self.N,
            'FirstFitHeuristic',
            self.graph_dir,
            self.seed
        )
        print()

        print("Step 5: Generating results and analysis...")
        all_results = firstfit_results + cbip_results + heuristic_results


        all_results.sort(key=lambda x: (x['algorithm'], x['k'], x['n']))

        generate_results_table(all_results, "results_table.csv")
        generate_markdown_table(all_results, "results_table.md")
        generate_latex_table(all_results, "results_table.tex")


if __name__ == "__main__":
    CsvGeneration().run()
