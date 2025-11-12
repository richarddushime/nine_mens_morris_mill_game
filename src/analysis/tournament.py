"""
Tournament system for testing different AI difficulties.
"""

import time
from typing import List, Dict
from famnit_gym.envs import mill
from src.ai.difficulties import MillAI, Difficulty


class Tournament:
    """
    Tournament system for running matches between AI agents.
    """
    
    def __init__(self):
        """Initialize tournament."""
        self.results = []
        self.match_history = []
    
    def run_match(self, 
                  ai1: MillAI, 
                  ai2: MillAI,
                  num_games: int = 10,
                  verbose: bool = True) -> Dict:
        """
        Run a match between two AI agents.
        
        Args:
            ai1: First AI agent
            ai2: Second AI agent
            num_games: Number of games to play
            verbose: Whether to print progress
        
        Returns:
            Dictionary with match results
        """
        wins_ai1 = 0
        wins_ai2 = 0
        draws = 0
        game_times = []
        
        for game_num in range(num_games):
            if verbose:
                print(f"Game {game_num + 1}/{num_games}...", end=" ")
            
            start_time = time.time()
            result = self._play_game(ai1, ai2)
            game_time = time.time() - start_time
            game_times.append(game_time)
            
            if result == 1:
                wins_ai1 += 1
                if verbose:
                    print(f"AI1 ({ai1.difficulty.value}) wins")
            elif result == 2:
                wins_ai2 += 1
                if verbose:
                    print(f"AI2 ({ai2.difficulty.value}) wins")
            else:
                draws += 1
                if verbose:
                    print("Draw")
        
        results = {
            'ai1_difficulty': ai1.difficulty.value,
            'ai2_difficulty': ai2.difficulty.value,
            'ai1_wins': wins_ai1,
            'ai2_wins': wins_ai2,
            'draws': draws,
            'total_games': num_games,
            'avg_game_time': sum(game_times) / len(game_times),
            'game_times': game_times
        }
        
        self.match_history.append(results)
        return results
    
    def _play_game(self, ai1: MillAI, ai2: MillAI) -> int:
        """
        Play a single game between two AIs.
        
        Args:
            ai1: First AI (plays as player 1)
            ai2: Second AI (plays as player 2)
        
        Returns:
            Winner (1, 2, or 0 for draw)
        """
        env = mill.env(render_mode=None)  # No rendering for speed
        env.reset()
        
        for agent in env.agent_iter():
            observation, reward, termination, truncation, info = env.last()
            
            if termination:
                # Game ended - determine winner
                if agent == "player_1":
                    return 2  # player_1 lost, so player_2 wins
                else:
                    return 1  # player_2 lost, so player_1 wins
            
            if truncation:
                return 0  # Draw (game too long)
            
            # Get current player
            player = 1 if agent == "player_1" else 2
            
            # Get transition model
            model = mill.transition_model(env)
            
            # Get move from appropriate AI
            if player == 1:
                move = ai1.get_move(model, player)
            else:
                move = ai2.get_move(model, player)
            
            env.step(move)
        
        return 0  # Draw
    
    def run_tournament(self, 
                      difficulties: List[Difficulty],
                      games_per_match: int = 2) -> Dict:
        """
        Run a round-robin tournament.
        
        Args:
            difficulties: List of difficulties to include
            games_per_match: Number of games per match
        
        Returns:
            Tournament results
        """
        results = {}
        
        for i, diff1 in enumerate(difficulties):
            for diff2 in difficulties[i:]:
                if diff1 == diff2:
                    continue
                
                ai1 = MillAI(difficulty=diff1)
                ai2 = MillAI(difficulty=diff2)
                
                match_result = self.run_match(ai1, ai2, games_per_match)
                
                key = f"{diff1.value}_vs_{diff2.value}"
                results[key] = match_result
        
        return results
    
    def print_results(self):
        """Print tournament results."""
        print("\n=== Tournament Results ===")
        for match in self.match_history:
            print(f"\n{match['ai1_difficulty']} vs {match['ai2_difficulty']}:")
            print(f"  AI1 wins: {match['ai1_wins']}")
            print(f"  AI2 wins: {match['ai2_wins']}")
            print(f"  Draws: {match['draws']}")
            print(f"  Avg game time: {match['avg_game_time']:.2f}s")

