# Bubble Shooter Game

A classic bubble shooter game implemented in Python using Pygame.

## Description
In this game, players shoot colored bubbles to match and pop groups of three or more bubbles of the same color. The goal is to clear the game board while preventing bubbles from reaching the bottom.

## Setup
1. Ensure you have Python 3.12 installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python src/main.py
   ```

## Development Setup
1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

The project uses:
- `black` for code formatting
- `ruff` for fast linting
- `mypy` for type checking

These checks run automatically on commit.

## Controls
- Mouse movement: Aim the shooter
- Left click: Shoot bubble
- ESC: Quit game

## Development Progress
- [x] Basic project setup
- [x] Game window and basic rendering
- [x] Bubble class implementation
- [x] Shooter mechanics
- [ ] Collision detection
- [ ] Bubble matching and popping
- [ ] Score system
- [ ] Game over conditions
- [ ] Sound effects and polish 