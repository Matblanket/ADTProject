from typing import List, Dict
import csv


def generate_results_table(results: List[Dict], output_file: str = "results_table.csv"):
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Algorithm', 'k', 'n', 'N', 
            'Average Competitive Ratio', 'Standard Deviation'
        ])
        
        for result in results:
            writer.writerow([
                result['algorithm'],
                result['k'],
                result['n'],
                result['N'],
                f"{result['avg_competitive_ratio']:.4f}",
                f"{result['std_dev']:.4f}"
            ])
    
    print(f"Results table saved to {output_file}")


def generate_markdown_table(results: List[Dict], output_file: str = "results_table.md"):
    with open(output_file, 'w') as f:
        f.write("| Algorithm | k | n | N | Average Competitive Ratio | Standard Deviation |\n")
        f.write("|:--|--:|--:|--:|--:|--:|\n")
        
        for result in results:
            f.write(f"| {result['algorithm']} | {result['k']} | {result['n']} | "
                   f"{result['N']} | {result['avg_competitive_ratio']:.4f} | "
                   f"{result['std_dev']:.4f} |\n")
    
    print(f"Markdown table saved to {output_file}")


def generate_latex_table(results: List[Dict], output_file: str = "results_table.tex"):
    with open(output_file, 'w') as f:
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\begin{tabular}{|l|c|c|c|c|c|}\n")
        f.write("\\hline\n")
        f.write("Algorithm & k & n & N & $\\overline{\\rho(Alg)}$ & $SD(\\rho(Alg))$ \\\\\n")
        f.write("\\hline\n")
        
        for result in results:
            f.write(f"{result['algorithm']} & {result['k']} & {result['n']} & "
                   f"{result['N']} & {result['avg_competitive_ratio']:.4f} & "
                   f"{result['std_dev']:.4f} \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\caption{Simulation Results}\n")
        f.write("\\end{table}\n")
    
    print(f"LaTeX table saved to {output_file}")

