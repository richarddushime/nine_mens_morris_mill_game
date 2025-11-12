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

**Important:** Only the famnit-gym package is used for the game environment, as required by the assignment.

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

## Documentation

- [Instructions for Running Examples](INSTRUCTIONS.md) - **Required for submission**

## Authors

**Dushime Mudahera Richard**

## License

This project is for educational purposes only.
