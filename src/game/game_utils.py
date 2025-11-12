"""
Utility functions for Mill game.
"""

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from famnit_gym.envs.mill.mill_model import MillModel


class GameUtils:
    """
    Utility functions for Mill game operations.
    """
    
    # Define all possible mill triplets
    # These are the positions that form mills (3 in a row)
    # Based on the actual MillModel implementation
    MILL_TRIPLETS = [
        # Horizontal mills
        [1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12],
        [13, 14, 15], [16, 17, 18], [19, 20, 21], [22, 23, 24],
        # Vertical mills
        [1, 10, 22], [4, 11, 19], [7, 12, 16], [2, 5, 8],
        [17, 20, 23], [9, 13, 18], [6, 14, 21], [3, 15, 24],
        # Diagonal mills
        [1, 4, 7], [3, 6, 9], [16, 19, 22], [18, 21, 24]
    ]
    
    @staticmethod
    def count_mills(model: 'MillModel', player: int) -> int:
        """
        Count the number of mills formed by a player.
        
        Args:
            model: Game state
            player: Player to count mills for (1 or 2)
        
        Returns:
            Number of mills
        """
        board = model.get_state()
        count = 0
        
        for mill in GameUtils.MILL_TRIPLETS:
            # Check if all positions in mill are occupied by player
            if all(1 <= pos <= 24 and board[pos - 1] == player for pos in mill):
                count += 1
        
        return count
    
    @staticmethod
    def count_threats(model: 'MillModel', player: int) -> int:
        """
        Count potential mills (two pieces, one empty).
        
        Args:
            model: Game state
            player: Player to count threats for
        
        Returns:
            Number of potential mills
        """
        board = model.get_state()
        count = 0
        
        for mill in GameUtils.MILL_TRIPLETS:
            player_count = sum(1 for pos in mill 
                             if 1 <= pos <= 24 and board[pos - 1] == player)
            empty_count = sum(1 for pos in mill 
                            if 1 <= pos <= 24 and board[pos - 1] == 0)
            
            if player_count == 2 and empty_count == 1:
                count += 1
        
        return count
    
    @staticmethod
    def calculate_mobility(model: 'MillModel', player: int) -> int:
        """
        Calculate mobility (number of legal moves).
        
        Args:
            model: Game state
            player: Player to calculate mobility for
        
        Returns:
            Number of legal moves
        """
        return len(model.legal_moves(player))
    
    @staticmethod
    def get_game_phase(model: 'MillModel', player: int) -> str:
        """
        Get current game phase for player.
        
        Args:
            model: Game state
            player: Player to get phase for
        
        Returns:
            Phase name ('placing', 'moving', 'flying', 'lost')
        """
        return model.get_phase(player)
    
    @staticmethod
    def format_move(move: List[int]) -> str:
        """
        Format move for display.
        
        Args:
            move: Move [src, dst, capture]
        
        Returns:
            Formatted string
        """
        src, dst, capture = move
        result = f"Move from {src} to {dst}"
        if capture > 0:
            result += f" (capture {capture})"
        return result
