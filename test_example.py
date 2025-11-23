"""
Test script to verify the implementation correctness.

This script tests the algorithms on a small example graph to ensure
they work correctly.
"""

from graph_generator import GraphGenerator
from coloring_algorithms import FirstFit, CBIP, FirstFitHeuristic


def test_small_example():
    """Test on a small graph (n=10, k=2)."""
    print("=" * 60)
    print("Testing on small example graph (n=10, k=2, p=0.5)")
    print("=" * 60)
    
    # Generate graph
    gen = GraphGenerator(n=10, k=2, p=0.5, seed=42)
    gen.generate()
    ordering = gen.get_online_ordering()
    
    print(f"\nGraph generated:")
    print(f"  Vertices: {gen.vertices}")
    print(f"  Number of edges: {len(gen.edges)}")
    print(f"  Online ordering: {ordering}")
    print(f"  Independent sets: {gen.independent_sets}")
    
    # Create neighbor function
    def get_neighbors(vertex: int, revealed: set) -> list:
        """Get neighbors of vertex that are in revealed set."""
        return gen.get_edges_for_vertex(vertex, revealed)
    
    # Test FirstFit
    print("\n" + "-" * 60)
    print("Testing FirstFit:")
    print("-" * 60)
    firstfit = FirstFit()
    coloring_ff = firstfit.color_online_graph(ordering, get_neighbors)
    print(f"  Colors used: {firstfit.get_num_colors()}")
    print(f"  Competitive ratio: {firstfit.get_num_colors() / 2:.4f}")
    print(f"  Coloring: {coloring_ff}")
    
    # Verify coloring is proper (no adjacent vertices have same color)
    is_proper = True
    for u, v in gen.edges:
        if coloring_ff.get(u) == coloring_ff.get(v):
            is_proper = False
            print(f"  ERROR: Vertices {u} and {v} have same color!")
    if is_proper:
        print("  [OK] Coloring is proper (no adjacent vertices have same color)")
    
    # Test CBIP
    print("\n" + "-" * 60)
    print("Testing CBIP:")
    print("-" * 60)
    cbip = CBIP(k=2)
    coloring_cbip = cbip.color_online_graph(ordering, get_neighbors)
    print(f"  Colors used: {cbip.get_num_colors()}")
    print(f"  Competitive ratio: {cbip.get_num_colors() / 2:.4f}")
    print(f"  Coloring: {coloring_cbip}")
    
    # Verify coloring is proper
    is_proper = True
    for u, v in gen.edges:
        if coloring_cbip.get(u) == coloring_cbip.get(v):
            is_proper = False
            print(f"  ERROR: Vertices {u} and {v} have same color!")
    if is_proper:
        print("  [OK] Coloring is proper")
    
    # Test FirstFitHeuristic
    print("\n" + "-" * 60)
    print("Testing FirstFitHeuristic:")
    print("-" * 60)
    heuristic = FirstFitHeuristic()
    coloring_heuristic = heuristic.color_online_graph(
        gen.vertices, gen.edges, get_neighbors
    )
    print(f"  Colors used: {heuristic.get_num_colors()}")
    print(f"  Competitive ratio: {heuristic.get_num_colors() / 2:.4f}")
    print(f"  Coloring: {coloring_heuristic}")
    
    # Verify coloring is proper
    is_proper = True
    for u, v in gen.edges:
        if coloring_heuristic.get(u) == coloring_heuristic.get(v):
            is_proper = False
            print(f"  ERROR: Vertices {u} and {v} have same color!")
    if is_proper:
        print("  [OK] Coloring is proper")
    
    print("\n" + "=" * 60)
    print("Test completed!")
    print("=" * 60)


if __name__ == "__main__":
    test_small_example()

