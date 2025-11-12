"""
Record AI vs AI gameplay video.
Useful for presentation demonstrations.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from famnit_gym.envs import mill
from famnit_gym.wrappers.mill import Video, DelayMove
from src.ai.difficulties import MillAI, Difficulty
import os


def main():
    """Record AI vs AI gameplay."""
    print("Recording AI vs AI gameplay video...")
    print("=" * 50)
    
    # Configuration
    ai1_difficulty = Difficulty.MEDIUM
    ai2_difficulty = Difficulty.HARD
    output_file = 'results/videos/ai_vs_ai_medium_hard.mp4'
    
    # Create output directory
    os.makedirs('results/videos', exist_ok=True)
    
    print(f"AI 1: {ai1_difficulty.value}")
    print(f"AI 2: {ai2_difficulty.value}")
    print(f"Output: {output_file}\n")
    
    # Create environment with video recording
    env = mill.env(render_mode='human')
    
    # Add delay between moves for better video viewing
    env = DelayMove(env, time_limit=2)  # 2 second delay between moves
    
    # Wrap with Video recorder
    env = Video(env, filename=output_file)
    
    env.reset()
    
    # Create AI agents
    ai1 = MillAI(difficulty=ai1_difficulty)
    ai2 = MillAI(difficulty=ai2_difficulty)
    
    print("Game started! Recording...")
    print("(Close window or wait for game to finish)\n")
    
    move_count = 0
    # Game loop
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        
        if termination:
            winner = "Player 2" if agent == "player_1" else "Player 1"
            print(f"\n{winner} wins!")
            break
        
        if truncation:
            print("\nGame ended (too long or window closed)")
            break
        
        # Get current player
        player = 1 if agent == "player_1" else 2
        
        # Get transition model
        model = mill.transition_model(env.unwrapped)
        
        # Get move from appropriate AI
        if player == 1:
            move = ai1.get_move(model, player)
            print(f"Move {move_count + 1}: Player 1 ({ai1_difficulty.value}) plays")
        else:
            move = ai2.get_move(model, player)
            print(f"Move {move_count + 1}: Player 2 ({ai2_difficulty.value}) plays")
        
        env.step(move)
        move_count += 1
    
    # Close environment (this generates the video)
    print("\nGenerating video...")
    env.close()
    
    print(f"\n✅ Video saved to: {output_file}")
    print(f"Total moves: {move_count}")


if __name__ == "__main__":
    main()

