"""
Different AI difficulty levels for Mill game.
"""

import random
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from famnit_gym.envs.mill.mill_model import MillModel
    from .utility import UtilityFunction
    from .minimax import MinimaxAI


class Difficulty(Enum):
    """AI difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class MillAI:
    """
    Mill AI agent with different difficulty levels.
    """
    
    def __init__(self, 
                 difficulty: Difficulty = Difficulty.HARD,
                 utility_function: 'UtilityFunction' = None,
                 custom_depth: int = None):
        """
        Initialize Mill AI agent.
        
        Args:
            difficulty: AI difficulty level
            utility_function: Custom utility function
            custom_depth: Custom search depth
        """
        self.difficulty = difficulty
        
        # Configure based on difficulty
        if difficulty == Difficulty.EASY:
            self.max_depth = 2
            self.random_prob = 0.3  # 30% random moves
            self.utility_weights = {
                'piece_weight': 5.0,
                'mill_weight': 30.0,
                'mobility_weight': 1.0,
                'phase_bonus': 2.0,
                'threat_weight': 5.0
            }
        elif difficulty == Difficulty.MEDIUM:
            self.max_depth = 4
            self.random_prob = 0.15  # 15% random moves
            self.utility_weights = {
                'piece_weight': 8.0,
                'mill_weight': 40.0,
                'mobility_weight': 1.5,
                'phase_bonus': 3.0,
                'threat_weight': 8.0
            }
        else:  # HARD
            self.max_depth = 6
            self.random_prob = 0.0  # No random moves
            self.utility_weights = {
                'piece_weight': 10.0,
                'mill_weight': 50.0,
                'mobility_weight': 2.0,
                'phase_bonus': 5.0,
                'threat_weight': 10.0
            }
        
        # Override depth if custom_depth is provided
        if custom_depth is not None:
            self.max_depth = custom_depth
        
        # Create utility function
        if utility_function is None:
            from .utility import UtilityFunction
            utility_function = UtilityFunction(**self.utility_weights)
        
        self.utility_function = utility_function
        
        # Create minimax AI
        from .minimax import MinimaxAI
        self.minimax_ai = MinimaxAI(
            utility_function=self.utility_function,
            max_depth=self.max_depth,
            use_alpha_beta=True
        )
    
    def get_move(self, model: 'MillModel', player: int) -> list:
        """
        Get the best move for the current game state.
        
        Args:
            model: Current game state (transition model)
            player: Current player (1 or 2)
        
        Returns:
            Best move [src, dst, capture]
        """
        legal_moves = model.legal_moves(player)
        
        if not legal_moves:
            return None
        
        # Random move with probability based on difficulty
        if random.random() < self.random_prob:
            return random.choice(legal_moves)
        
        # Use minimax to find best move
        best_move, _ = self.minimax_ai.get_best_move(model, player)
        
        return best_move
    
    def get_statistics(self) -> dict:
        """
        Get AI statistics from last move.
        
        Returns:
            Dictionary with statistics
        """
        stats = self.minimax_ai.get_statistics()
        stats['difficulty'] = self.difficulty.value
        stats['max_depth'] = self.max_depth
        stats['random_prob'] = self.random_prob
        return stats
