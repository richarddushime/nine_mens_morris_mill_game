"""
Human vs AI gameplay example.
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from famnit_gym.envs import mill
from famnit_gym.wrappers.mill import UserInteraction
from src.ai.difficulties import MillAI, Difficulty


def main():
    """Run human vs AI game."""
    # Create environment with user interaction
    env = mill.env(render_mode='human')
    env = UserInteraction(env)
    env.reset()
    
    # Create AI agent
    ai = MillAI(difficulty=Difficulty.MEDIUM)
    
    print("Human vs AI Game")
    print("Instructions:")
    print("  - Placing phase: Click on empty position to place piece")
    print("  - Moving phase: Click source, then destination")
    print("  - Press SPACE to skip your turn (let AI move)")
    print("  - Press ESC to quit")
    print("\nYou are Player 1, AI is Player 2\n")
    
    # Game loop
    for agent in env.agent_iter():
        observation, reward, termination, truncation, info = env.last()
        
        if termination:
            if agent == "player_1":
                print("\nYou lost! AI wins.")
            else:
                print("\nYou won! Congratulations!")
            break
        
        if truncation:
            print("\nGame ended")
            break
        
        # Get current player
        player = 1 if agent == "player_1" else 2
        
        if player == 1:
            # Human player's turn
            print(f"\nYour turn (Player {player})")
            print(f"Phase: {info.get('phase', 'unknown')}")
            
            # Get legal moves and phase
            legal_moves = info['legal_moves']
            phase = info.get('phase', 'placing')
            
            # Mark legal destination positions based on phase
            if phase == 'placing':
                # In placing phase, mark only empty positions where we can place
                board = env.observe(agent)
                for [src, dst, capture] in legal_moves:
                    if src == 0 and board[dst - 1] == 0:  # Only mark empty positions
                        env.mark_position(dst, (128, 128, 0, 128))  # Yellow shade
            else:
                # In moving/flying phase, mark all legal destinations
                for [src, dst, capture] in legal_moves:
                    env.mark_position(dst, (128, 128, 0, 128))  # Yellow shade for destinations
            
            selected_src = None
            done = False
            
            if phase == 'placing':
                # In placing phase, just click destination (src is always 0)
                print("Click on a highlighted position to place your piece")
                while not done:
                    interaction = env.interact()
                    
                    if interaction.get('type') == 'quit':
                        return
                    
                    if interaction.get('type') == 'mouse_click':
                        position = interaction.get('position', 0)
                        if position == 0:
                            continue
                        
                        # Find move with this destination
                        move = None
                        for legal_move in legal_moves:
                            if legal_move[0] == 0 and legal_move[1] == position:
                                move = legal_move
                                break
                        
                        if move is not None:
                            env.clear_markings()
                            env.step(move)
                            print(f"Placed piece at position {position}")
                            done = True
                        else:
                            print(f"Invalid position {position}. Try again.")
                    
                    elif interaction.get('type') == 'key_press':
                        key = interaction.get('key')
                        if key == 'space':
                            # Skip turn - let AI move
                            env.clear_markings()
                            env.step(None)
                            done = True
                        elif key == 'escape':
                            return
            
            else:
                # Moving or flying phase - need source and destination
                print("Click your piece (source), then a highlighted destination")
                while not done:
                    interaction = env.interact()
                    
                    if interaction.get('type') == 'quit':
                        return
                    
                    if interaction.get('type') == 'mouse_click':
                        position = interaction.get('position', 0)
                        if position == 0:
                            continue
                        
                        if selected_src is None:
                            # Check if this position has our piece
                            board = env.observe(agent)
                            if board[position - 1] == 1:  # Our piece
                                selected_src = position
                                env.mark_position(position, (0, 255, 0, 128))  # Green for selected
                                print(f"Selected source: {position}")
                                # Re-mark only destinations for this source
                                env.clear_markings()
                                env.mark_position(position, (0, 255, 0, 128))  # Keep source marked
                                for [src, dst, capture] in legal_moves:
                                    if src == selected_src:
                                        env.mark_position(dst, (128, 128, 0, 128))  # Yellow for destinations
                            else:
                                print(f"Position {position} doesn't have your piece. Try again.")
                        else:
                            selected_dst = position
                            print(f"Selected destination: {position}")
                            
                            # Try to make move
                            move = None
                            for legal_move in legal_moves:
                                if legal_move[0] == selected_src and legal_move[1] == selected_dst:
                                    move = legal_move
                                    break
                            
                            if move is None:
                                print("Invalid move! Try again.")
                                env.clear_markings()
                                # Re-mark all destinations
                                for [src, dst, capture] in legal_moves:
                                    env.mark_position(dst, (128, 128, 0, 128))
                                selected_src = None
                            else:
                                env.clear_markings()
                                env.step(move)
                                print(f"Moved from {selected_src} to {selected_dst}")
                                done = True
                    
                    elif interaction.get('type') == 'key_press':
                        key = interaction.get('key')
                        if key == 'space':
                            # Skip turn or cancel selection
                            if selected_src is not None:
                                env.clear_markings()
                                # Re-mark all destinations
                                for [src, dst, capture] in legal_moves:
                                    env.mark_position(dst, (128, 128, 0, 128))
                                selected_src = None
                                print("Selection cancelled")
                            else:
                                # Skip turn - let AI move
                                env.clear_markings()
                                env.step(None)
                                done = True
                        elif key == 'escape':
                            return
        
        else:
            # AI player's turn
            print(f"\nAI's turn (Player {player})")
            # Use unwrapped environment for transition model
            model = mill.transition_model(env.unwrapped)
            move = ai.get_move(model, player)
            print(f"AI moves: {move}")
            env.step(move)
    
    env.close()


if __name__ == "__main__":
    main()
