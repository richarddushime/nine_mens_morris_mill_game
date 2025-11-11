"""
Tests for minimax algorithm.
"""

import pytest
from src.ai.minimax import MinimaxAI
from src.ai.utility import UtilityFunction


def test_minimax_initialization():
    """Test minimax AI initialization."""
    utility = UtilityFunction()
    ai = MinimaxAI(utility_function=utility, max_depth=3)
    
    assert ai.max_depth == 3
    assert ai.use_alpha_beta == True
    assert ai.utility_function == utility


def test_minimax_statistics():
    """Test that statistics are tracked."""
    utility = UtilityFunction()
    ai = MinimaxAI(utility_function=utility, max_depth=2)
    
    stats = ai.get_statistics()
    
    assert 'nodes_evaluated' in stats
    assert 'pruning_count' in stats
    assert 'pruning_ratio' in stats


