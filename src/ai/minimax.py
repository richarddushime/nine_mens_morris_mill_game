"""
Minimax algorithm with alpha-beta pruning for Mill game.
"""

import math
from typing import TYPE_CHECKING, List, Tuple, Optional

if TYPE_CHECKING:
    from famnit_gym.envs.mill.mill_model import MillModel
    from .utility import UtilityFunction


class MinimaxAI:
    """
    Minimax AI with alpha-beta pruning for Mill game.
    """
    
    def __init__(self, 
                 utility_function: 'UtilityFunction',
                 max_depth: int = 5,
                 use_alpha_beta: bool = True):
        """
        Initialize Minimax AI.
        
        Args:
            utility_function: Function to evaluate board positions
            max_depth: Maximum search depth
            use_alpha_beta: Whether to use alpha-beta pruning
        """
        self.utility_function = utility_function
        self.max_depth = max_depth
        self.use_alpha_beta = use_alpha_beta
        self.nodes_evaluated = 0
        self.pruning_count = 0
    
    def get_best_move(self, 
                     model: 'MillModel', 
                     player: int) -> Tuple[List[int], float]:
        """
        Find the best move using minimax algorithm.
        
        Args:
            model: Current game state (transition model)
            player: Current player (1 or 2)
        
        Returns:
            Tuple of (best_move, evaluation_score)
        """
        self.nodes_evaluated = 0
        self.pruning_count = 0
        
        legal_moves = model.legal_moves(player)
        
        if not legal_moves:
            return None, -math.inf if player == 1 else math.inf
        
        best_move = None
        best_value = -math.inf if player == 1 else math.inf
        
        for move in legal_moves:
            # Clone model and make move
            new_model = model.clone()
            new_model.make_move(player, move)
            
            # Evaluate position
            if self.use_alpha_beta:
                value = self._minimax_ab(
                    new_model,
                    self.max_depth - 1,
                    -math.inf,
                    math.inf,
                    player == 1,  # True if maximizing
                    2 if player == 1 else 1  # Opponent
                )
            else:
                value = self._minimax(
                    new_model,
                    self.max_depth - 1,
                    player == 1,
                    2 if player == 1 else 1
                )
            
            # Update best move
            if player == 1:  # Maximizing
                if value > best_value:
                    best_value = value
                    best_move = move
            else:  # Minimizing
                if value < best_value:
                    best_value = value
                    best_move = move
        
        return best_move, best_value
    
    def _minimax(self, 
                model: 'MillModel',
                depth: int,
                maximizing: bool,
                current_player: int) -> float:
        """
        Basic minimax algorithm (without alpha-beta).
        
        Args:
            model: Current game state
            depth: Remaining search depth
            maximizing: True if maximizing player's turn
            current_player: Current player (1 or 2)
        
        Returns:
            Evaluation score
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0 or model.game_over():
            # Evaluate from perspective of player 1
            return self.utility_function.evaluate(model, 1)
        
        legal_moves = model.legal_moves(current_player)
        
        if not legal_moves:
            # No legal moves - evaluate current position
            return self.utility_function.evaluate(model, 1)
        
        opponent = 2 if current_player == 1 else 1
        
        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                new_model = model.clone()
                new_model.make_move(current_player, move)
                eval_score = self._minimax(
                    new_model,
                    depth - 1,
                    False,
                    opponent
                )
                max_eval = max(max_eval, eval_score)
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                new_model = model.clone()
                new_model.make_move(current_player, move)
                eval_score = self._minimax(
                    new_model,
                    depth - 1,
                    True,
                    opponent
                )
                min_eval = min(min_eval, eval_score)
            return min_eval
    
    def _minimax_ab(self,
                   model: 'MillModel',
                   depth: int,
                   alpha: float,
                   beta: float,
                   maximizing: bool,
                   current_player: int) -> float:
        """
        Minimax with alpha-beta pruning.
        
        Args:
            model: Current game state
            depth: Remaining search depth
            alpha: Best value for maximizing player
            beta: Best value for minimizing player
            maximizing: True if maximizing player's turn
            current_player: Current player (1 or 2)
        
        Returns:
            Evaluation score
        """
        self.nodes_evaluated += 1
        
        # Terminal conditions
        if depth == 0 or model.game_over():
            return self.utility_function.evaluate(model, 1)
        
        legal_moves = model.legal_moves(current_player)
        
        if not legal_moves:
            return self.utility_function.evaluate(model, 1)
        
        opponent = 2 if current_player == 1 else 1
        
        if maximizing:
            max_eval = -math.inf
            for move in legal_moves:
                new_model = model.clone()
                new_model.make_move(current_player, move)
                eval_score = self._minimax_ab(
                    new_model,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    opponent
                )
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    self.pruning_count += 1
                    break
            
            return max_eval
        else:
            min_eval = math.inf
            for move in legal_moves:
                new_model = model.clone()
                new_model.make_move(current_player, move)
                eval_score = self._minimax_ab(
                    new_model,
                    depth - 1,
                    alpha,
                    beta,
                    True,
                    opponent
                )
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                # Alpha-beta pruning
                if beta <= alpha:
                    self.pruning_count += 1
                    break
            
            return min_eval
    
    def get_statistics(self) -> dict:
        """
        Get search statistics.
        
        Returns:
            Dictionary with search statistics
        """
        return {
            'nodes_evaluated': self.nodes_evaluated,
            'pruning_count': self.pruning_count,
            'pruning_ratio': (self.pruning_count / self.nodes_evaluated 
                            if self.nodes_evaluated > 0 else 0)
        }

