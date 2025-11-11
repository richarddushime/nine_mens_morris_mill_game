# Nine Men's Morris (Mill) Game

An intelligent agent implementation for playing Nine Men's Morris using adversarial search algorithms.

## Overview

This project implements an AI agent for Nine Men's Morris (Mill) game using:
- **Minimax algorithm** with alpha-beta pruning
- **Multiple difficulty levels** (Easy, Medium, Hard)
- **Human-AI gameplay** support
- **Performance analysis** and tournament system

## Requirements

- Python 3.8+
- famnit-gym package (required by assignment)
- numpy, gymnasium, pettingzoo (dependencies of famnit-gym)
- matplotlib (for generating performance plots)

**Important:** All search algorithms (minimax, alpha-beta pruning) are implemented from scratch in Python. No external AI or search libraries are used. Only the famnit-gym package is used for the game environment, as required by the assignment.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/richarddushime/nine_mens_morris_mill_game.git
cd nine_mens_morris_mill_game
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install famnit-gym:
```bash
pip install famnit_gym@git+https://github.com/DomenSoberlFamnit/famnit-gym
```

## Project Structure

```
nine_mens_morris_mill_game/
├── src/              # Source code
│   ├── ai/          # AI algorithms
│   ├── game/        # Game logic
│   └── analysis/    # Analysis tools
├── examples/         # Example scripts
├── tests/           # Unit tests
└── results/         # results
```

## Quick Start

### Basic AI vs AI Game
```bash
python examples/basic_game.py
```

### Human vs AI
```bash
python examples/human_vs_ai.py
```

### Run Tournament
```bash
python examples/tournament.py
```

### Analyze Search Depth Performance
```bash
python examples/depth_analysis.py
```

## Features

### 1. Adversarial Search
- Minimax algorithm with alpha-beta pruning
- Configurable search depth
- Custom utility functions

### 2. Multiple Difficulty Levels
- **Easy**: Random moves with limited search depth
- **Medium**: Occasional mistakes, moderate depth
- **Hard**: Full minimax with optimal depth

### 3. Human Interaction
- Play against AI using mouse/keyboard
- Visual board representation
- Move validation

### 4. Analysis Tools
- Depth vs time performance plots
- Self-play analysis
- Tournament statistics

## Implementation Details

### 1. Adversarial Search (Requirement 1)

#### Minimax Algorithm with Alpha-Beta Pruning
- **Location**: `src/ai/minimax.py`
- **Implementation**: Fully self-implemented in Python
- **Features**:
  - Minimax algorithm with configurable depth
  - Alpha-beta pruning for performance optimization
  - Statistics tracking (nodes evaluated, pruning count)

#### Utility Function
- **Location**: `src/ai/utility.py`
- **Components**:
  - **Piece count**: `(my_pieces - opponent_pieces) × 10`
  - **Mills**: `(my_mills - opponent_mills) × 50`
  - **Mobility**: `(my_moves - opponent_moves) × 2`
  - **Phase bonus**: Extra points for placing phase
  - **Threats**: Potential mills that can be formed
- **Weights**: Configurable per difficulty level

#### Depth Limiting
- **Analysis**: Run `python examples/depth_analysis.py`
- **Output**: Plots showing search time vs depth, nodes evaluated vs depth
- **Optimal depth**: Determined through testing (typically 5-6 for real-time play)

#### Self-Play Testing
- **Script**: `examples/self_play.py`
- **Purpose**: Test perfect AI vs perfect AI (should result in draws)
- **Expected**: High draw rate indicates strong AI play

### 2. Different Difficulties (Requirement 2)

Three difficulty levels implemented in `src/ai/difficulties.py`:

- **Easy**:
  - Search depth: 2
  - Random move probability: 30%
  - Simplified utility weights
  
- **Medium**:
  - Search depth: 4
  - Random move probability: 15%
  - Improved utility weights
  
- **Hard**:
  - Search depth: 6
  - Random move probability: 0%
  - Optimal utility weights

**Tournament**: Run `python examples/tournament.py` to compare difficulties

### 3. Human Interaction (Requirement 3)

- **Implementation**: `examples/human_vs_ai.py`
- **Wrapper**: Uses `UserInteraction` from famnit-gym
- **Controls**: Mouse clicks for move selection
- **Testing**: Play against any difficulty level to test if you can beat the AI

## Results

See `results/` directory for:
- Performance plots
- Tournament results
- Game logs

## Testing

Run tests:
```bash
python -m pytest tests/
```

## Submission Requirements

This project meets all seminar requirements:

1. ✅ **Adversarial Search**: Minimax with alpha-beta pruning, utility function documented, depth analysis with plots, self-play testing
2. ✅ **Different Difficulties**: Three difficulty levels implemented, tournament comparison
3. ✅ **Human Interaction**: User Interaction wrapper implemented, playable against AI
4. ✅ **Source Code**: All algorithms self-implemented in Python, only famnit-gym used for environment

## Submission Files

For submission, create:
1. **ZIP file** with all Python code
2. **PDF poster** presenting findings
3. **INSTRUCTIONS.md** (this file) - instructions on how to run examples

**Naming pattern**: `<group number>_IS_Seminar1_<last name 1>_<last name 2>.[zip | pdf | md]`

## Documentation

- [Instructions for Running Examples](INSTRUCTIONS.md) - **Required for submission**

## Authors

Dushime Mudahera Richard

## License

This project is for educational purposes only.
