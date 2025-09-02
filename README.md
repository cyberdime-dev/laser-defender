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
  - **H Key**: View high scores
  - **ESC Key**: Clear high scores (when viewing high score screen)
- **Scoring**: +1 point for each target destroyed
- **Game Over**: Occurs when any target reaches the bottom of the screen

## Features

- Player-controlled paddle movement
- Laser shooting mechanics with cooldown
- 5 different laser visual styles
- Falling target waves
- Real-time score tracking
- Advanced high score system with statistics and rankings
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

This project is licensed under the MIT License - see below for details:

```
MIT License

Copyright (c) 2024 Laser Defender

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests
- Improve documentation

## Acknowledgments

- Built with [Pygame](https://www.pygame.org/)
- Inspired by classic arcade shooters
- Thanks to the Pygame community for excellent documentation :D
