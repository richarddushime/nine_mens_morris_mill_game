"""
Record Human vs AI gameplay video.
Useful for presentation demonstrations.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from famnit_gym.envs import mill
from famnit_gym.wrappers.mill import Video, UserInteraction, DelayMove
from src.ai.difficulties import MillAI, Difficulty
import os


def main():
    """Record Human vs AI gameplay."""
    print("Recording Human vs AI gameplay video...")
    print("=" * 50)
    
    # Configuration
    ai_difficulty = Difficulty.MEDIUM
    output_file = 'results/videos/human_vs_ai_medium.mp4'
    human_is_player_1 = True  # Human plays first
    
    # Create output directory
    os.makedirs('results/videos', exist_ok=True)
    
    print(f"Human: Player {'1' if human_is_player_1 else '2'}")
    print(f"AI: Player {'2' if human_is_player_1 else '1'} ({ai_difficulty.value})")
    print(f"Output: {output_file}\n")
    
    # Create environment
    env = mill.env(render_mode='human')
    
    # Add user interaction for human player
    env = UserInteraction(env)
    
    # Add delay for AI moves (so video is watchable)
    env = DelayMove(env, time_limit=1)  # 1 second delay for AI moves
    
    # Wrap with Video recorder
    env = Video(env, filename=output_file)
    
    env.reset()
    
    # Create AI agent
    ai = MillAI(difficulty=ai_difficulty)
    
    print("Game started! Recording...")
    print("Instructions:")
    print("  - Click positions to make moves")
    print("  - SPACE: Skip/cancel selection")
    print("  - Close window to end recording\n")
    
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
        is_human = (player == 1 and human_is_player_1) or (player == 2 and not human_is_player_1)
        
        if is_human:
            # Human player - get interaction
            print(f"Move {move_count + 1}: Your turn (Player {player})")
            interaction = env.interact()
            
            # Extract move from interaction
            if interaction and 'move' in interaction:
                move = interaction['move']
                if move:
                    env.step(move)
                    move_count += 1
            else:
                # User cancelled or closed window
                break
        else:
            # AI player
            print(f"Move {move_count + 1}: AI thinking (Player {player})...")
            
            # Get transition model
            model = mill.transition_model(env.unwrapped)
            
            # Get AI move
            move = ai.get_move(model, player)
            
            if move:
                env.step(move)
                move_count += 1
            else:
                print("AI has no moves!")
                break
    
    # Close environment (this generates the video)
    print("\nGenerating video...")
    env.close()
    
    print(f"\n✅ Video saved to: {output_file}")
    print(f"Total moves: {move_count}")


if __name__ == "__main__":
    main()

