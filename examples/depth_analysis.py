"""
Analyze search depth vs performance.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.statistics import Statistics
import os


def main():
    """Analyze depth performance and create plots."""
    print("Analyzing search depth performance...")
    print("This may take a few minutes...\n")
    
    # Analyze depth performance
    # Reduced parameters for faster execution:
    # - max_depth=6: Test depths 1-6 (depth 7+ takes too long)
    # - num_tests=3: Fewer tests per depth for speed
    data = Statistics.analyze_depth_performance(max_depth=6, num_tests=3)
    
    # Print results
    print("\nDepth Analysis Results:")
    print("-" * 50)
    for i, depth in enumerate(data['depths']):
        print(f"Depth {depth}: "
              f"Avg Time: {data['avg_times'][i]:.3f}s, "
              f"Nodes: {int(data['nodes_evaluated'][i])}")
    
    # Create plots
    os.makedirs('results/plots', exist_ok=True)
    Statistics.plot_depth_analysis(data, 'results/plots/depth_analysis.png')
    
    print("\nPlot saved to results/plots/depth_analysis.png")


if __name__ == "__main__":
    main()
