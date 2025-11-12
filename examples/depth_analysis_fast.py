"""
Fast depth analysis - optimized for quick results.
Tests fewer depths and fewer iterations.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.statistics import Statistics
import os


def main():
    """Fast depth analysis with reduced parameters."""
    print("Fast Depth Analysis (optimized for speed)")
    print("=" * 50)
    print("Testing depths 1-5 with 2 tests per depth")
    print("This should complete in 1-2 minutes...\n")
    
    # Fast analysis: depth 1-5, 2 tests each
    data = Statistics.analyze_depth_performance(max_depth=5, num_tests=2)
    
    # Print results
    print("\n" + "=" * 50)
    print("Depth Analysis Results:")
    print("-" * 50)
    for i, depth in enumerate(data['depths']):
        print(f"Depth {depth}: "
              f"Avg Time: {data['avg_times'][i]:.3f}s, "
              f"Nodes: {int(data['nodes_evaluated'][i])}")
    
    # Create plots
    os.makedirs('results/plots', exist_ok=True)
    Statistics.plot_depth_analysis(data, 'results/plots/depth_analysis.png')
    
    print("\n✅ Plot saved to results/plots/depth_analysis.png")
    print("\nNote: For more comprehensive analysis, use examples/depth_analysis.py")


if __name__ == "__main__":
    main()
