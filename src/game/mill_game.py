"""
Game state management for Mill.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from famnit_gym.envs.mill.mill_model import MillModel


class MillGame:
    """
    Wrapper for managing Mill game state.
    """
    
    def __init__(self, model: 'MillModel'):
        """
        Initialize game with transition model.
        
        Args:
            model: Mill transition model
        """
        self.model = model
    
    def get_current_player(self) -> int:
        """
        Get current player (1 or 2).
        
        Returns:
            Current player number
        """
        # This would need to be tracked separately
        # For now, return based on game state
        return 1  # Placeholder
    
    def is_game_over(self) -> bool:
        """
        Check if game is over.
        
        Returns:
            True if game is over
        """
        return self.model.game_over()
    
    def get_legal_moves(self, player: int) -> list:
        """
        Get legal moves for player.
        
        Args:
            player: Player number (1 or 2)
        
        Returns:
            List of legal moves
        """
        return self.model.legal_moves(player)
    
    def make_move(self, player: int, move: list) -> dict:
        """
        Make a move in the game.
        
        Args:
            player: Player making the move
            move: Move [src, dst, capture]
        
        Returns:
            Move information
        """
        return self.model.make_move(player, move)
    
    def clone(self) -> 'MillGame':
        """
        Create a copy of the game state.
        
        Returns:
            Cloned game state
        """
        return MillGame(self.model.clone())

