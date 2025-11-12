"""
Basic AI vs AI game example.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from famnit_gym.envs import mill
from src.ai.difficulties import MillAI, Difficulty


def main():
    """Run a basic AI vs AI game."""
    # Create environment
    env = mill.env(render_mode='human')
    env.reset()
    
    # Create AI agents
    ai1 = MillAI(difficulty=Difficulty.MEDIUM)
    ai2 = MillAI(difficulty=Difficulty.HARD)
    
    print("Starting game: Medium AI (Player 1) vs Hard AI (Player 2)")
    print("Close the window to exit.\n")
    
    # Game loop
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        
        if termination:
            winner = "Player 2" if agent == "player_1" else "Player 1"
            print(f"\n{winner} wins!")
            break
        
        if truncation:
            print("\nGame ended in a draw (too long)")
            break
        
        # Get current player
        player = 1 if agent == "player_1" else 2
        
        # Get transition model
        model = mill.transition_model(env)
        
        # Get move from appropriate AI
        if player == 1:
            move = ai1.get_move(model, player)
            print(f"Player 1 (Medium): {move}")
        else:
            move = ai2.get_move(model, player)
            print(f"Player 2 (Hard): {move}")
        
        env.step(move)
    
    env.close()


if __name__ == "__main__":
    main()
