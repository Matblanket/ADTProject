import math
import statistics
from typing import List, Dict, Tuple, Optional
import os


class FunctionFittingAnalysis:
   
    def __init__(self):
        self.results = []
   
    def load_results_from_csv(self, csv_file: str = "results_table.csv") -> List[Dict]:
        self.results = []
        try:
            with open(csv_file, 'r') as f:
                lines = f.readlines()
                if not lines:
                    return self.results
                   
                headers = [h.strip() for h in lines[0].strip().split(',')]
                for line in lines[1:]:
                    if not line.strip():
                        continue
                    values = line.strip().split(',')
                    if len(values) != len(headers):
                        continue
                       
                    result = {}
                    for i, header in enumerate(headers):
                        try:
                            if header in ['Algorithm']:
                                result[header.lower()] = values[i]
                            elif header in ['k', 'n', 'N']:
                                result[header] = int(values[i])
                            elif header in ['Average Competitive Ratio', 'Standard Deviation']:
                                result[header.lower().replace(' ', '_')] = float(values[i])
                            else:
                                result[header.lower().replace(' ', '_')] = values[i]
                        except (ValueError, IndexError):
                            continue
                   
                    self.results.append(result)


        except FileNotFoundError:
            print(f"Warning: {csv_file} not found")


        return self.results
   
    def analyze_all_results(self) -> str:
        if not self.results:
            return "No results available for analysis."
       
        report = "FUNCTION FITTING AND TREND ANALYSIS REPORT\n"
        report += "=" * 70 + "\n\n"
       
        grouped_data = self._group_results()
       
        for (algo, k), algo_results in grouped_data.items():
            report += self._analyze_algorithm_group(algo, k, algo_results)
       
        report += self._generate_comparative_analysis(grouped_data)
        report += self._generate_overall_observations(grouped_data)
       
        return report
   
    def _group_results(self) -> Dict[Tuple[str, int], List[Dict]]:
        grouped = {}
        for result in self.results:
            key = (result['algorithm'], result['k'])
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(result)
       
        for key in grouped:
            grouped[key].sort(key=lambda x: x['n'])
       
        return grouped
   
    def _analyze_algorithm_group(self, algorithm: str, k: int, results: List[Dict]) -> str:
        if len(results) < 2:
            return f"Insufficient data for {algorithm} with k={k}\n\n"
       
        n_values = [r['n'] for r in results]
        ratios = [r['average_competitive_ratio'] for r in results]
       
        analysis = f"{algorithm} ALGORITHM (k={k})\n"
        analysis += "-" * 50 + "\n"
        analysis += self._generate_basic_stats(n_values, ratios)
        analysis += self._generate_text_plot(n_values, ratios)
        analysis += self._perform_function_fitting(n_values, ratios)
        analysis += self._analyze_trends(n_values, ratios)       
        analysis += "\n" + "=" * 50 + "\n\n"
        return analysis
   
    def _generate_basic_stats(self, n_values: List[int], ratios: List[float]) -> str:
        stats = "Basic Statistics:\n"
        stats += f"  Sample size: {len(n_values)} data points\n"
        stats += f"  n range: {min(n_values)} to {max(n_values)}\n"
        stats += f"  Ratio range: {min(ratios):.3f} to {max(ratios):.3f}\n"
        stats += f"  Mean ratio: {statistics.mean(ratios):.3f}\n"
        stats += f"  Std deviation: {statistics.stdev(ratios) if len(ratios) > 1 else 0:.3f}\n"
        stats += f"  Coefficient of variation: {(statistics.stdev(ratios)/statistics.mean(ratios)*100) if len(ratios) > 1 and statistics.mean(ratios) != 0 else 0:.1f}%\n\n"
        return stats
   
    def _generate_text_plot(self, n_values: List[int], ratios: List[float]) -> str:
        if not n_values:
            return ""
       
        plot = "Data Visualization:\n"
        plot += "n        Ratio    Visual\n"
        plot += "-------- -------- " + "-" * 30 + "\n"
       
        min_ratio = min(ratios)
        max_ratio = max(ratios)
        range_ratio = max_ratio - min_ratio if max_ratio != min_ratio else 1
       
        for i, n in enumerate(n_values):
            ratio = ratios[i]
            bar_length = int(((ratio - min_ratio) / range_ratio) * 30)
            bar = "█" * bar_length
            plot += f"{n:8} {ratio:8.3f} {bar}\n"
       
        plot += "\n"
        return plot
   
    def _perform_function_fitting(self, n_values: List[int], ratios: List[float]) -> str:
        if len(n_values) < 3:
            return "Insufficient data points for function fitting.\n\n"
       
        analysis = "Function Fitting Analysis:\n"
       
        fits = []
       
        constant_fit = self._fit_constant(n_values, ratios)
        fits.append(constant_fit)
       
        linear_fit = self._fit_linear(n_values, ratios)
        if linear_fit:
            fits.append(linear_fit)
       
        log_fit = self._fit_logarithmic(n_values, ratios)
        if log_fit:
            fits.append(log_fit)
       
        sqrt_fit = self._fit_square_root(n_values, ratios)
        if sqrt_fit:
            fits.append(sqrt_fit)
       
        quadratic_fit = self._fit_quadratic(n_values, ratios)
        if quadratic_fit:
            fits.append(quadratic_fit)
       
        fits.sort(key=lambda x: x['r_squared'], reverse=True)
       
        analysis += "  Function        | Equation              | R²     | Quality\n"
        analysis += "  --------------- | --------------------- | ------ | --------\n"
       
        for fit in fits:
            quality = self._get_fit_quality(fit['r_squared'])
            analysis += f"  {fit['name']:14} | {fit['equation']:20} | {fit['r_squared']:6.3f} | {quality}\n"
       
        if fits and fits[0]['r_squared'] > 0:
            best_fit = fits[0]
            analysis += f"\n  Best fit: {best_fit['name']} (R² = {best_fit['r_squared']:.3f})\n"
            analysis += self._interpret_fit(best_fit, n_values, ratios)
       
        analysis += "\n"
        return analysis
   
    def _fit_constant(self, n_values: List[int], ratios: List[float]) -> Dict:
        constant = statistics.mean(ratios)
        ss_res = sum((r - constant) ** 2 for r in ratios)
        ss_tot = sum((r - statistics.mean(ratios)) ** 2 for r in ratios)
        r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
       
        return {
            'name': 'Constant',
            'equation': f"y = {constant:.3f}",
            'r_squared': r_squared,
            'function_type': 'constant'
        }
   
    def _fit_linear(self, n_values: List[int], ratios: List[float]) -> Optional[Dict]:
        if len(set(n_values)) < 2:
            return None
           
        try:
            n_mean = statistics.mean(n_values)
            r_mean = statistics.mean(ratios)
           
            numerator = sum((n_values[i] - n_mean) * (ratios[i] - r_mean) for i in range(len(n_values)))
            denominator = sum((n_values[i] - n_mean) ** 2 for i in range(len(n_values)))
           
            if denominator == 0:
                return None
               
            a = numerator / denominator
            b = r_mean - a * n_mean
           
            predicted = [a * n + b for n in n_values]
            ss_res = sum((ratios[i] - predicted[i]) ** 2 for i in range(len(n_values)))
            ss_tot = sum((r - r_mean) ** 2 for r in ratios)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
           
            return {
                'name': 'Linear',
                'equation': f"y = {a:.6f}n + {b:.3f}",
                'r_squared': r_squared,
                'function_type': 'linear',
                'slope': a
            }
        except:
            return None
   
    def _fit_logarithmic(self, n_values: List[int], ratios: List[float]) -> Optional[Dict]:
        try:
            log_n = [math.log(n) for n in n_values]
            if len(set(log_n)) < 2:
                return None
               
            log_mean = statistics.mean(log_n)
            r_mean = statistics.mean(ratios)
           
            numerator = sum((log_n[i] - log_mean) * (ratios[i] - r_mean) for i in range(len(n_values)))
            denominator = sum((log_n[i] - log_mean) ** 2 for i in range(len(n_values)))
           
            if denominator == 0:
                return None
               
            a = numerator / denominator
            b = r_mean - a * log_mean
           
            predicted = [a * math.log(n) + b for n in n_values]
            ss_res = sum((ratios[i] - predicted[i]) ** 2 for i in range(len(n_values)))
            ss_tot = sum((r - r_mean) ** 2 for r in ratios)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
           
            return {
                'name': 'Logarithmic',
                'equation': f"y = {a:.3f}*log(n) + {b:.3f}",
                'r_squared': r_squared,
                'function_type': 'logarithmic'
            }
        except:
            return None
   
    def _fit_square_root(self, n_values: List[int], ratios: List[float]) -> Optional[Dict]:
        try:
            sqrt_n = [math.sqrt(n) for n in n_values]
            if len(set(sqrt_n)) < 2:
                return None
               
            sqrt_mean = statistics.mean(sqrt_n)
            r_mean = statistics.mean(ratios)
           
            numerator = sum((sqrt_n[i] - sqrt_mean) * (ratios[i] - r_mean) for i in range(len(n_values)))
            denominator = sum((sqrt_n[i] - sqrt_mean) ** 2 for i in range(len(n_values)))
           
            if denominator == 0:
                return None
               
            a = numerator / denominator
            b = r_mean - a * sqrt_mean
           
            predicted = [a * math.sqrt(n) + b for n in n_values]
            ss_res = sum((ratios[i] - predicted[i]) ** 2 for i in range(len(n_values)))
            ss_tot = sum((r - r_mean) ** 2 for r in ratios)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
           
            return {
                'name': 'Square Root',
                'equation': f"y = {a:.3f}*sqrt(n) + {b:.3f}",
                'r_squared': r_squared,
                'function_type': 'square_root'
            }
        except:
            return None
   
    def _fit_quadratic(self, n_values: List[int], ratios: List[float]) -> Optional[Dict]:
        if len(n_values) < 3:
            return None
           
        try:
            n_squared = [n**2 for n in n_values]
            sum_n = sum(n_values)
            sum_n2 = sum(n_squared)
            sum_n3 = sum(n**3 for n in n_values)
            sum_n4 = sum(n**4 for n in n_values)
            sum_r = sum(ratios)
            sum_nr = sum(n_values[i] * ratios[i] for i in range(len(n_values)))
            sum_n2r = sum(n_squared[i] * ratios[i] for i in range(len(n_values)))
            denom = len(n_values) * sum_n2 * sum_n4 + 2 * sum_n * sum_n2 * sum_n3 - sum_n2**3 - len(n_values) * sum_n3**2 - sum_n**2 * sum_n4
           
            if abs(denom) < 1e-10:
                return None
               
            a = (len(n_values) * sum_n2 * sum_n2r + sum_n * sum_n3 * sum_r + sum_n * sum_n2 * sum_nr -
                 sum_n2**2 * sum_r - len(n_values) * sum_n3 * sum_nr - sum_n**2 * sum_n2r) / denom
           
            b = (len(n_values) * sum_n4 * sum_nr + sum_n * sum_n2 * sum_n2r + sum_n2 * sum_n3 * sum_r -
                 sum_n2 * sum_n4 * sum_r - len(n_values) * sum_n3 * sum_n2r - sum_n * sum_n3 * sum_nr) / denom
           
            c = (sum_n2 * sum_n4 * sum_r + sum_n * sum_n3 * sum_nr + sum_n2 * sum_n3 * sum_n2r -
                 sum_n2**2 * sum_n2r - sum_n * sum_n4 * sum_nr - sum_n3**2 * sum_r) / denom
           
            predicted = [a * n**2 + b * n + c for n in n_values]
            r_mean = statistics.mean(ratios)
            ss_res = sum((ratios[i] - predicted[i]) ** 2 for i in range(len(n_values)))
            ss_tot = sum((r - r_mean) ** 2 for r in ratios)
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
           
            return {
                'name': 'Quadratic',
                'equation': f"y = {a:.6f}n² + {b:.3f}n + {c:.3f}",
                'r_squared': r_squared,
                'function_type': 'quadratic'
            }
        except:
            return None
   
    def _get_fit_quality(self, r_squared: float) -> str:
        if r_squared >= 0.9:
            return "Excellent"
        elif r_squared >= 0.7:
            return "Good"
        elif r_squared >= 0.5:
            return "Moderate"
        elif r_squared >= 0.3:
            return "Weak"
        else:
            return "Poor"
   
    def _interpret_fit(self, fit: Dict, n_values: List[int], ratios: List[float]) -> str:
        interpretation = "  Interpretation: "
        if fit['function_type'] == 'constant':
            interpretation += "Performance is scale-invariant; graph size doesn't affect competitive ratio.\n"
       
        elif fit['function_type'] == 'linear':
            slope = fit.get('slope', 0)
            if abs(slope) < 1e-6:
                interpretation += "Negligible linear trend; essentially constant.\n"
            elif slope > 0:
                interpretation += f"Competitive ratio increases linearly with graph size (slope = {slope:.6f}).\n"
            else:
                interpretation += f"Competitive ratio decreases linearly with graph size (slope = {slope:.6f}).\n"
       
        elif fit['function_type'] == 'logarithmic':
            interpretation += "Performance follows logarithmic scaling; improves slowly with larger graphs.\n"
       
        elif fit['function_type'] == 'square_root':
            interpretation += "Performance follows square root scaling; moderate dependence on graph size.\n"
       
        elif fit['function_type'] == 'quadratic':
            interpretation += "Performance shows quadratic relationship with graph size.\n"
       
        if len(ratios) >= 2:
            trend = ratios[-1] - ratios[0]
            if abs(trend) < 0.05:
                interpretation += "  Overall trend: Stable across graph sizes.\n"
            elif trend > 0:
                interpretation += f"  Overall trend: Increasing (+{trend:.3f} from smallest to largest graph).\n"
            else:
                interpretation += f"  Overall trend: Decreasing ({trend:.3f} from smallest to largest graph).\n"
       
        return interpretation
   
    def _analyze_trends(self, n_values: List[int], ratios: List[float]) -> str:
        if len(ratios) < 2:
            return ""
       
        analysis = "Trend Analysis:\n"
        overall_change = ratios[-1] - ratios[0]
        change_percentage = (overall_change / ratios[0]) * 100 if ratios[0] != 0 else 0
       
        if abs(overall_change) < 0.01:
            analysis += "  Overall: Stable (minimal change across graph sizes)\n"
        elif overall_change > 0:
            analysis += f"  Overall: Increasing (+{overall_change:.3f}, {change_percentage:+.1f}%)\n"
        else:
            analysis += f"  Overall: Decreasing ({overall_change:.3f}, {change_percentage:+.1f}%)\n"
       
        increasing_segments = 0
        decreasing_segments = 0
        stable_segments = 0
       
        for i in range(1, len(ratios)):
            local_change = ratios[i] - ratios[i-1]
            if abs(local_change) < 0.005:
                stable_segments += 1
            elif local_change > 0:
                increasing_segments += 1
            else:
                decreasing_segments += 1
       
        analysis += f"  Local trends: {increasing_segments} increasing, {decreasing_segments} decreasing, {stable_segments} stable segments\n"

        if len(ratios) > 1:
            cv = (statistics.stdev(ratios) / statistics.mean(ratios)) * 100
            analysis += f"  Variability: Coefficient of variation = {cv:.1f}% "
            if cv < 10:
                analysis += "(Low variability)\n"
            elif cv < 25:
                analysis += "(Moderate variability)\n"
            else:
                analysis += "(High variability)\n"
       
        return analysis
   
    def _generate_comparative_analysis(self, grouped_data: Dict) -> str:
        analysis = "\nCOMPARATIVE ANALYSIS ACROSS ALGORITHMS\n"
        analysis += "=" * 60 + "\n\n"
        k_values = sorted(set(k for _, k in grouped_data.keys()))
       
        for k in k_values:
            analysis += f"k = {k}:\n"
            analysis += "-" * 40 + "\n"
           
            algorithms = [algo for algo, k_val in grouped_data.keys() if k_val == k]
            if not algorithms:
                continue
               
            analysis += "Algorithm           | Avg Ratio | Trend  | Best Fit\n"
            analysis += "--------------------|-----------|--------|----------\n"
           
            for algo in sorted(algorithms):
                results = grouped_data[(algo, k)]
                results.sort(key=lambda x: x['n'])
               
                avg_ratio = statistics.mean([r['average_competitive_ratio'] for r in results])
                trend = self._calculate_trend_direction([r['average_competitive_ratio'] for r in results])
                best_fit = self._get_best_fit_name([r['n'] for r in results], [r['average_competitive_ratio'] for r in results])
               
                analysis += f"{algo:18} | {avg_ratio:9.3f} | {trend:6} | {best_fit}\n"
           
            analysis += "\n"
       
        return analysis
   
    def _calculate_trend_direction(self, ratios: List[float]) -> str:
        if len(ratios) < 2:
            return "N/A"
       
        change = ratios[-1] - ratios[0]
        if abs(change) < 0.01:
            return "Stable"
        elif change > 0:
            return "Up"
        else:
            return "Down"
   
    def _get_best_fit_name(self, n_values: List[int], ratios: List[float]) -> str:
        if len(n_values) < 3:
            return "Insufficient data"
        fits = []
       
        constant_fit = self._fit_constant(n_values, ratios)
        if constant_fit:
            fits.append(constant_fit)
       
        linear_fit = self._fit_linear(n_values, ratios)
        if linear_fit:
            fits.append(linear_fit)
       
        if fits:
            best_fit = max(fits, key=lambda x: x['r_squared'])
            return best_fit['name']
       
        return "Unknown"
   
    def _generate_overall_observations(self, grouped_data: Dict) -> str:
        observations = "\nOVERALL OBSERVATIONS AND CONCLUSIONS\n"
        observations += "=" * 60 + "\n\n"
        observations += "KEY FINDINGS:\n\n"
        cbip_results = [r for (algo, k), results in grouped_data.items() for r in results if algo == 'CBIP']
        if cbip_results:
            cbip_ratios = [r['average_competitive_ratio'] for r in cbip_results]
            if all(abs(r - 1.0) < 0.001 for r in cbip_ratios):
                observations += "• CBIP achieves perfect competitive ratio (1.0) for all bipartite graphs,\n"
                observations += "  confirming theoretical optimality for k=2.\n\n"

        firstfit_results = [r for (algo, k), results in grouped_data.items() for r in results if 'FirstFit' in algo]
        if firstfit_results:
            observations += "• FirstFit algorithms show varying performance:\n"
           
            for k in [2, 3, 4]:
                standard_ff = [r for (algo, k_val), results in grouped_data.items() for r in results
                              if algo == 'FirstFit' and k_val == k]
                heuristic_ff = [r for (algo, k_val), results in grouped_data.items() for r in results
                               if algo == 'FirstFitHeuristic' and k_val == k]
               
                if standard_ff and heuristic_ff:
                    std_avg = statistics.mean([r['average_competitive_ratio'] for r in standard_ff])
                    heur_avg = statistics.mean([r['average_competitive_ratio'] for r in heuristic_ff])
                    improvement = ((std_avg - heur_avg) / std_avg) * 100
                   
                    if improvement > 0:
                        observations += f"  - k={k}: Heuristic improves performance by {improvement:.1f}%\n"
                    else:
                        observations += f"  - k={k}: Heuristic shows similar performance\n"
            observations += "\n"
       
        observations += "SCALABILITY ANALYSIS:\n\n"
       
        for (algo, k), results in grouped_data.items():
            if len(results) < 3:
                continue
               
            ratios = [r['average_competitive_ratio'] for r in results]
            trend = self._calculate_trend_direction(ratios)
           
            if trend == "Stable":
                observations += f"• {algo} (k={k}): Performance is scale-invariant\n"
            elif trend == "Up":
                observations += f"• {algo} (k={k}): Performance degrades with larger graphs\n"
            else:
                observations += f"• {algo} (k={k}): Performance improves with larger graphs\n"
       
        observations += "\nFUNCTION FITTING SUMMARY:\n\n"
        fit_summary = {}
        for (algo, k), results in grouped_data.items():
            if len(results) < 3:
                continue
               
            n_vals = [r['n'] for r in results]
            ratios = [r['average_competitive_ratio'] for r in results]
            best_fit = self._get_best_fit_name(n_vals, ratios)
           
            if best_fit not in fit_summary:
                fit_summary[best_fit] = []
            fit_summary[best_fit].append(f"{algo} (k={k})")
       
        for fit_type, algorithms in fit_summary.items():
            observations += f"• {fit_type} fit: {', '.join(algorithms)}\n"
       
        return observations


def main():
    analyzer = FunctionFittingAnalysis()
    print("Loading results from results_table.csv...")
    results = analyzer.load_results_from_csv()
   
    if not results:
        print("No results found. Please ensure results_table.csv exists.")
        return
   
    print(f"Loaded {len(results)} data points")
    print("\nGenerating analysis report...")
    report = analyzer.analyze_all_results()
    with open("function_fitting_analysis.txt", "w", encoding="utf-8") as f:
        f.write(report)
   
    print("Analysis complete! Saved to function_fitting_analysis.txt")
    print("\n" + "=" * 70)
    print(report)


if __name__ == "__main__":
    main()

