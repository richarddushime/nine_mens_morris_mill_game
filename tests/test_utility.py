"""
Tests for utility function.
"""

import pytest
from src.ai.utility import UtilityFunction


def test_utility_initialization():
    """Test utility function initialization."""
    utility = UtilityFunction(
        piece_weight=10.0,
        mill_weight=50.0,
        mobility_weight=2.0
    )
    
    assert utility.piece_weight == 10.0
    assert utility.mill_weight == 50.0
    assert utility.mobility_weight == 2.0


