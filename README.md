# Laser Defender

A simple arcade-style paddle shooter game built with Python and Pygame. Control a paddle at the bottom of the screen to shoot lasers at falling targets before they reach the bottom.

## Gameplay

- **Objective**: Shoot down falling red targets with green lasers
- **Controls**: 
  - **Left/Right Arrow Keys**: Move paddle horizontally
  - **Spacebar**: Shoot laser (with cooldown)
  - **R Key**: Restart game when game over
  - **1-5 Keys**: Change laser visual style
  - **M Key**: Toggle background music on/off
- **Scoring**: +1 point for each target destroyed
- **Game Over**: Occurs when any target reaches the bottom of the screen

## Features

- Player-controlled paddle movement
- Laser shooting mechanics with cooldown
- 5 different laser visual styles
- Falling target waves
- Real-time score tracking
- Sound effects (shooting, hits, game over)
- Background music with toggle
- Game over and restart functionality

## Requirements

- Python 3.7+
- Pygame 2.6.1

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/laser-defender.git
   cd laser-defender
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the game:**
   ```bash
   python laser_defender.py
   ```

## Alternative Setup (Virtual Environment)

For isolated development:

```bash
# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt

# Run game
python laser_defender.py
```

## Troubleshooting

### Pygame Installation Issues
If you encounter build errors on Linux:

```bash
sudo apt update
sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
pip install pygame==2.6.1
```

### Display Issues
- Ensure you're running in a desktop environment (not SSH/headless)
- Game runs at 600x800 resolution at 60 FPS

## Development

The game is built as a single Python file (`laser_defender.py`) with:
- Main game loop with event handling
- Paddle movement and laser shooting mechanics
- Target spawning and collision detection
- Score tracking and game state management

## License

[Add your license here]
