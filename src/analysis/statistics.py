"""
Statistics and analysis tools.
"""

import time
import matplotlib.pyplot as plt
from typing import List, Dict
from src.ai.difficulties import MillAI, Difficulty
from src.ai.minimax import MinimaxAI


class Statistics:
    """
    Statistics collection and visualization.
    """
    
    @staticmethod
    def analyze_depth_performance(max_depth: int = 6, 
                                  num_tests: int = 3) -> Dict:
        """
        Analyze search performance vs depth.
        
        Args:
            max_depth: Maximum depth to test (recommended: 6 or less)
            num_tests: Number of test positions per depth (recommended: 3 or less)
        
        Returns:
            Dictionary with depth vs time data
        """
        from famnit_gym.envs import mill
        
        depths = list(range(1, max_depth + 1))
        avg_times = []
        nodes_evaluated = []
        
        env = mill.env(render_mode=None)
        env.reset()
        
        print(f"Testing depths 1-{max_depth} with {num_tests} tests per depth...")
        print("Progress: ", end="", flush=True)
        
        for depth in depths:
            print(f"Depth {depth}... ", end="", flush=True)
            times = []
            total_nodes = 0
            
            for test_num in range(num_tests):
                model = mill.transition_model(env)
                player = 1
                
                ai = MillAI(difficulty=Difficulty.HARD)
                ai.minimax_ai.max_depth = depth
                
                start_time = time.time()
                move, _ = ai.minimax_ai.get_best_move(model, player)
                elapsed = time.time() - start_time
                
                times.append(elapsed)
                total_nodes += ai.minimax_ai.nodes_evaluated
                
                # Show progress for each test
                print(f"({test_num+1}/{num_tests}) ", end="", flush=True)
            
            avg_times.append(sum(times) / len(times))
            nodes_evaluated.append(total_nodes / num_tests)
            print(f"Done (avg: {avg_times[-1]:.2f}s)", flush=True)
        
        return {
            'depths': depths,
            'avg_times': avg_times,
            'nodes_evaluated': nodes_evaluated
        }
    
    @staticmethod
    def plot_depth_analysis(data: Dict, save_path: str = None):
        """
        Plot depth vs time analysis.
        
        Args:
            data: Data from analyze_depth_performance
            save_path: Path to save plot (optional)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Plot 1: Time vs Depth
        ax1.plot(data['depths'], data['avg_times'], 'b-o')
        ax1.set_xlabel('Search Depth')
        ax1.set_ylabel('Average Time (seconds)')
        ax1.set_title('Search Time vs Depth')
        ax1.grid(True)
        
        # Plot 2: Nodes Evaluated vs Depth
        ax2.plot(data['depths'], data['nodes_evaluated'], 'r-o')
        ax2.set_xlabel('Search Depth')
        ax2.set_ylabel('Nodes Evaluated')
        ax2.set_title('Nodes Evaluated vs Depth')
        ax2.grid(True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
    
    @staticmethod
    def analyze_self_play(num_games: int = 20) -> Dict:
        """
        Analyze self-play (perfect AI vs perfect AI).
        
        Args:
            num_games: Number of games to play
        
        Returns:
            Statistics dictionary
        """
        from src.analysis.tournament import Tournament
        
        tournament = Tournament()
        ai1 = MillAI(difficulty=Difficulty.HARD)
        ai2 = MillAI(difficulty=Difficulty.HARD)
        
        results = tournament.run_match(ai1, ai2, num_games, verbose=False)
        
        return {
            'total_games': results['total_games'],
            'draws': results['draws'],
            'draw_rate': results['draws'] / results['total_games'],
            'avg_game_time': results['avg_game_time']
        }

