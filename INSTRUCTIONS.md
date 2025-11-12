# Instructions for Running Examples

This document provides instructions on how to run the examples for the Nine Men's Morris (Mill) AI implementation.

## Prerequisites

1. **Python 3.8 or higher** must be installed on your system.

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   pip install famnit_gym@git+https://github.com/DomenSoberlFamnit/famnit-gym
   ```

   Note: The `requirements.txt` includes dependencies needed for the famnit-gym package (gymnasium, pettingzoo, numpy) and matplotlib for generating plots. All search algorithms (minimax, alpha-beta pruning) are implemented from scratch in Python without using any external AI/search libraries.

## Running Examples

All examples should be run from the project root directory (`nine_mens_morris_mill_game/`).

### 1. Basic AI vs AI Game

Run a game between two AI agents:

```bash
python examples/basic_game.py
```

This will:
- Start a visual game window
- Play a game between Medium AI (Player 1) and Hard AI (Player 2)
- Display moves in the console
- Show the winner when the game ends

**Expected output:** Console messages showing each player's moves and the final winner.

### 2. Human vs AI Gameplay

Play against an AI agent:

```bash
python examples/human_vs_ai.py
```

**Controls:**
- **Mouse click**: Click on board positions to select source and destination
- **SPACE key**: Skip your turn (let AI move)
- **ESC key**: Quit the game

**Instructions:**
1. You are Player 1, AI is Player 2
2. Click on a position to select it as source
3. Click on another position to select it as destination
4. The move will be executed if valid
5. AI will automatically make its move after yours

### 3. Tournament - Difficulty Comparison

Run a tournament between different AI difficulty levels:

```bash
python examples/tournament.py
```

This will:
- Run matches between Easy, Medium, and Hard AI difficulties
- Play 10 games per match
- Display results in the console
- Save results to `results/statistics/tournament_results.json`

**Expected output:** Tournament results showing wins, losses, and draws for each difficulty matchup.

### 4. Search Depth Analysis

Analyze how search depth affects performance:

```bash
python examples/depth_analysis.py
```

This will:
- Test search depths from 1 to 8
- Measure average time per move and nodes evaluated
- Generate plots showing:
  - Search time vs depth
  - Nodes evaluated vs depth
- Save plots to `results/plots/depth_analysis.png`

**Note:** This may take several minutes to complete.

**Expected output:** Console output with depth analysis results and saved plot files.

### 5. Self-Play Analysis

Test perfect AI vs perfect AI:

```bash
python examples/self_play.py
```

This will:
- Run 20 games between two Hard AI agents
- Analyze draw rate (perfect play should result in draws)
- Display statistics

**Expected output:** Statistics showing total games, draws, draw rate, and average game time.

## Project Structure

```
nine_mens_morris_mill_game/
├── src/                    # Source code (all algorithms self-implemented)
│   ├── ai/                 # AI algorithms
│   │   ├── minimax.py      # Minimax with alpha-beta pruning
│   │   ├── utility.py      # Utility function
│   │   └── difficulties.py # Difficulty levels
│   ├── game/               # Game utilities
│   └── analysis/           # Analysis tools
├── examples/                # Example scripts
│   ├── basic_game.py       # AI vs AI
│   ├── human_vs_ai.py      # Human vs AI
│   ├── tournament.py       # Tournament
│   ├── depth_analysis.py    # Depth analysis
│   └── self_play.py        # Self-play
└── results/                 # Generated results
    ├── plots/              # Performance plots
    └── statistics/         # Tournament results
```

## Implementation Notes

### Adversarial Search (Requirement 1)
- **Minimax algorithm**: Implemented in `src/ai/minimax.py`
- **Alpha-beta pruning**: Included in minimax implementation
- **Utility function**: Defined in `src/ai/utility.py` with components:
  - Piece count difference
  - Number of mills formed
  - Mobility (available moves)
  - Phase bonuses
  - Threat detection
- **Depth limiting**: Configurable via `max_depth` parameter
- **Depth analysis**: Run `examples/depth_analysis.py` for plots
- **Self-play**: Run `examples/self_play.py` to test perfect AI vs perfect AI

### Different Difficulties (Requirement 2)
- **Three difficulty levels**: Easy, Medium, Hard (implemented in `src/ai/difficulties.py`)
- **Easy**: Limited depth (2), 30% random moves
- **Medium**: Moderate depth (4), 15% random moves
- **Hard**: Full depth (6), no random moves
- **Tournament**: Run `examples/tournament.py` to compare difficulties

### Human Interaction (Requirement 3)
- **User Interaction wrapper**: Used in `examples/human_vs_ai.py`
- **Controls**: Mouse clicks and keyboard input
- **Play against any difficulty**: Modify the difficulty in `human_vs_ai.py`

## Troubleshooting

### Performance Issues
If examples run too slowly:
- Reduce search depth in difficulty settings
- Reduce number of games in tournament
- Use `render_mode=None` for faster execution (modify examples)

## Contact

For questions or issues, refer to the main README.md
