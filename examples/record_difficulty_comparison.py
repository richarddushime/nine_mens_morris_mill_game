"""
Record short gameplay videos comparing different AI difficulties.
Creates multiple short videos for presentation.
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


def record_short_game(ai1_difficulty, ai2_difficulty, output_file, max_moves=20):
    """Record a short game between two AIs."""
    print(f"\nRecording: {ai1_difficulty.value} vs {ai2_difficulty.value}")
    
    # Create environment
    env = mill.env(render_mode='human')
    env = DelayMove(env, time_limit=1)  # 1 second delay
    env = Video(env, filename=output_file)
    env.reset()
    
    # Create AIs
    ai1 = MillAI(difficulty=ai1_difficulty)
    ai2 = MillAI(difficulty=ai2_difficulty)
    
    move_count = 0
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        
        if termination or truncation or move_count >= max_moves:
            break
        
        player = 1 if agent == "player_1" else 2
        model = mill.transition_model(env.unwrapped)
        
        if player == 1:
            move = ai1.get_move(model, player)
        else:
            move = ai2.get_move(model, player)
        
        if move:
            env.step(move)
            move_count += 1
        else:
            break
    
    env.close()
    print(f"  ✅ Saved: {output_file} ({move_count} moves)")


def main():
    """Record multiple short comparison videos."""
    print("Recording Difficulty Comparison Videos")
    print("=" * 50)
    print("Creating short gameplay clips for presentation...\n")
    
    # Create output directory
    os.makedirs('results/videos', exist_ok=True)
    
    # Record different matchups
    matchups = [
        (Difficulty.EASY, Difficulty.MEDIUM, 'easy_vs_medium.mp4'),
        (Difficulty.MEDIUM, Difficulty.HARD, 'medium_vs_hard.mp4'),
        (Difficulty.EASY, Difficulty.HARD, 'easy_vs_hard.mp4'),
    ]
    
    for ai1, ai2, filename in matchups:
        output_file = f'results/videos/{filename}'
        record_short_game(ai1, ai2, output_file, max_moves=15)
    
    print("\n" + "=" * 50)
    print("✅ All videos saved to results/videos/")
    print("\nVideos created:")
    for _, _, filename in matchups:
        print(f"  - {filename}")


if __name__ == "__main__":
    main()

