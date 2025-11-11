"""
Tests for difficulty levels.
"""

import pytest
from src.ai.difficulties import MillAI, Difficulty


def test_difficulty_initialization():
    """Test AI difficulty initialization."""
    ai_easy = MillAI(difficulty=Difficulty.EASY)
    ai_medium = MillAI(difficulty=Difficulty.MEDIUM)
    ai_hard = MillAI(difficulty=Difficulty.HARD)
    
    assert ai_easy.difficulty == Difficulty.EASY
    assert ai_medium.difficulty == Difficulty.MEDIUM
    assert ai_hard.difficulty == Difficulty.HARD
    
    assert ai_easy.max_depth <= ai_medium.max_depth
    assert ai_medium.max_depth <= ai_hard.max_depth
    
    assert ai_easy.random_prob >= ai_medium.random_prob
    assert ai_medium.random_prob >= ai_hard.random_prob



