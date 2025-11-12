"""
Tournament example - run matches between different AI difficulties.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.tournament import Tournament
from src.ai.difficulties import Difficulty


def main():
    """Run a tournament between different difficulties."""
    tournament = Tournament()
    
    # Run matches between all difficulty levels
    difficulties = [Difficulty.EASY, Difficulty.MEDIUM, Difficulty.HARD]
    
    print("Starting tournament...")
    print("=" * 50)
    
    results = tournament.run_tournament(difficulties, games_per_match=2)
    
    # Print results
    tournament.print_results()
    
    # Save results to file
    import json
    import os
    os.makedirs('results/statistics', exist_ok=True)
    with open('results/statistics/tournament_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults saved to results/statistics/tournament_results.json")


if __name__ == "__main__":
    main()
