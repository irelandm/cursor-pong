# Pong Game

A classic Pong game implementation using Python and pygame-ce (Community Edition). This project features a modular design with separate components for game entities, utilities, and game logic.

## Features

- Classic Pong gameplay with two paddles and a ball
- Score tracking and win conditions
- Ball speed increases after paddle hits
- Realistic ball deflection based on paddle contact point
- Clean, modular code structure
- Comprehensive test suite

## Project Structure

```
pong_game/
├── __init__.py
├── main.py
├── entities/
│   ├── __init__.py
│   ├── ball.py
│   ├── game_state.py
│   └── paddle.py
└── utils/
    ├── __init__.py
    └── constants.py
```

### Components

- `main.py`: Entry point for the game, handles game loop and rendering
- `entities/`: Contains game objects
  - `ball.py`: Ball physics and collision logic
  - `paddle.py`: Paddle movement and collision detection
  - `game_state.py`: Score tracking and game state management
- `utils/`: Contains game constants and helper functions
  - `constants.py`: Game configuration values

## Requirements

- Python 3.6+
- pygame-ce (Community Edition)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pong.git
cd pong
```

2. Install dependencies using pipenv:
```bash
pipenv install
```

## Running the Game

Using pipenv:
```bash
# To suppress Pipenv warnings, set this environment variable:
export PIPENV_VERBOSITY=-1
pipenv run start
```

Or directly:
```bash
python -m pong_game.main
```

## Controls

- Left Paddle:
  - W: Move up
  - S: Move down
- Right Paddle:
  - Up Arrow: Move up
  - Down Arrow: Move down
- R: Restart game when game over

## Testing

Using pipenv:
```bash
pipenv run test
```

Or directly:
```bash
python -m unittest test_pong.py
```

## Code Quality and Linting

This project uses flake8 for code quality checks. The configuration is defined in `.flake8`.

### Linting Rules

The project follows these linting rules:
- Maximum line length: 100 characters
- Docstrings required for public modules, classes, and methods
- No trailing whitespace
- Files must end with a newline
- Additional checks from bugbear (B) and docstring (D) plugins

### Running Linting

Using pipenv:
```bash
pipenv run lint
```

Or to check a specific file:
```bash
pipenv run lint-ball
```

Or directly:
```bash
flake8 pong_game/
flake8 pong_game/entities/ball.py
```

### Common Linting Issues

- W291: Trailing whitespace
- W292: Missing newline at end of file
- D100: Missing docstring in public module
- D101: Missing docstring in public class
- D102: Missing docstring in public method

## Game Rules

1. Players control paddles on either side of the screen
2. Score points by getting the ball past the opponent's paddle
3. Ball speed increases after each paddle hit
4. First player to reach 3 points wins
5. Press R to restart after game over

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 