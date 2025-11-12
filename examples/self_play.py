"""
Self-play analysis - perfect AI vs perfect AI.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.analysis.statistics import Statistics


def main():
    """Run self-play analysis."""
    print("Running self-play analysis (Hard AI vs Hard AI)...")
    print("This may take a while...\n")
    
    results = Statistics.analyze_self_play(num_games=4)
    
    print("\nSelf-Play Results:")
    print("-" * 50)
    print(f"Total games: {results['total_games']}")
    print(f"Draws: {results['draws']}")
    print(f"Draw rate: {results['draw_rate']:.2%}")
    print(f"Average game time: {results['avg_game_time']:.2f}s")
    
    print("\nNote: With perfect play, games should end in draws.")
    print(f"Draw rate of {results['draw_rate']:.2%} indicates AI quality.")


if __name__ == "__main__":
    main()

