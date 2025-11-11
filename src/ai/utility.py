"""
Utility function for evaluating Mill game states.
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from famnit_gym.envs.mill.mill_model import MillModel


class UtilityFunction:
    """
    Evaluates board positions for the Mill game.
    
    Components:
    - Piece count: Difference in pieces on board
    - Mills: Number of mills formed
    - Mobility: Number of legal moves available
    - Phase bonuses: Extra points for different game phases
    - Threats: Potential mills that can be formed
    """
    
    def __init__(self, 
                 piece_weight: float = 10.0,
                 mill_weight: float = 50.0,
                 mobility_weight: float = 2.0,
                 phase_bonus: float = 5.0,
                 threat_weight: float = 10.0):
        """
        Initialize utility function with weights.
        
        Args:
            piece_weight: Weight for piece count difference
            mill_weight: Weight for mill count difference
            mobility_weight: Weight for mobility difference
            phase_bonus: Bonus for being in placing phase
            threat_weight: Weight for potential mills
        """
        self.piece_weight = piece_weight
        self.mill_weight = mill_weight
        self.mobility_weight = mobility_weight
        self.phase_bonus = phase_bonus
        self.threat_weight = threat_weight
    
    def evaluate(self, model: 'MillModel', player: int) -> float:
        """
        Evaluate the board position for the given player.
        
        Args:
            model: The game state (transition model)
            player: Player to evaluate for (1 or 2)
        
        Returns:
            Evaluation score (higher is better for player)
        """
        opponent = 2 if player == 1 else 1
        
        # Component 1: Piece count
        my_pieces = model.count_pieces(player)
        opp_pieces = model.count_pieces(opponent)
        piece_score = (my_pieces - opp_pieces) * self.piece_weight
        
        # Component 2: Mills
        my_mills = self._count_mills(model, player)
        opp_mills = self._count_mills(model, opponent)
        mill_score = (my_mills - opp_mills) * self.mill_weight
        
        # Component 3: Mobility
        my_moves = len(model.legal_moves(player))
        opp_moves = len(model.legal_moves(opponent))
        mobility_score = (my_moves - opp_moves) * self.mobility_weight
        
        # Component 4: Phase bonus
        phase_score = 0.0
        my_phase = model.get_phase(player)
        if my_phase == 'placing':
            phase_score = self.phase_bonus
        
        # Component 5: Threats (potential mills)
        my_threats = self._count_threats(model, player)
        opp_threats = self._count_threats(model, opponent)
        threat_score = (my_threats - opp_threats) * self.threat_weight
        
        # Total score
        total_score = (piece_score + mill_score + mobility_score + 
                      phase_score + threat_score)
        
        return total_score
    
    def _count_mills(self, model: 'MillModel', player: int) -> int:
        """
        Count the number of mills formed by the player.
        
        Args:
            model: The game state
            player: Player to count mills for
        
        Returns:
            Number of mills
        """
        from src.game.game_utils import GameUtils
        mills = GameUtils.MILL_TRIPLETS
        
        count = 0
        board = model.get_state()
        
        for mill in mills:
            # Check if all three positions in mill are occupied by player
            if all(1 <= pos <= 24 and board[pos - 1] == player for pos in mill):
                count += 1
        
        return count
    
    def _count_threats(self, model: 'MillModel', player: int) -> int:
        """
        Count potential mills (two pieces, one empty spot).
        
        Args:
            model: The game state
            player: Player to count threats for
        
        Returns:
            Number of potential mills
        """
        from src.game.game_utils import GameUtils
        mills = GameUtils.MILL_TRIPLETS
        threats = 0
        board = model.get_state()
        
        for mill in mills:
            player_count = sum(1 for pos in mill 
                             if 1 <= pos <= 24 and board[pos - 1] == player)
            empty_count = sum(1 for pos in mill 
                            if 1 <= pos <= 24 and board[pos - 1] == 0)
            
            if player_count == 2 and empty_count == 1:
                threats += 1
        
        return threats

