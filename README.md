# Uno Game

A robust Python implementation of the classic Uno card game, featuring a flexible game engine, command-line interface, and AI opponents.

## Features

*   **Flexible Engine**: Designed to support custom rules and extensions.
*   **Command-Line Interface (CLI)**: Playable terminal-based game against bots.
*   **AI Opponents**: Includes `RandomPlayer` bots to play against.
*   **Type Safe**: Built with modern Python type hinting for reliability.
*   **Tested**: Comprehensive test suite using `pytest`.

## Installation

Requires Python 3.11 or higher.

1.  Clone the repository:
    ```bash
    git clone https://github.com/Dorapower/Uno-Game.git
    cd Uno-Game
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -e .
    pip install pytest
    ```

## Usage

To start a game against bots via the CLI:

```bash
python src/cli.py
```

Follow the on-screen prompts to choose the number of players and make your moves.

## Development

### Running Tests

The project uses `pytest` for testing. To run the test suite:

```bash
pytest
```

### Project Structure

*   `src/uno/engine`: Core game logic (Game, Player, Context).
*   `src/uno/rules`: Rule implementations (Standard Uno).
*   `src/cli.py`: Command-line interface entry point.
*   `tests/`: Unit tests.

## Rules

This implementation follows the standard Uno rules (based on the 2008 instruction sheet).
- **Setup**: 7 cards per player.
- **Objective**: Be the first to get rid of all your cards.
- **Action Cards**: Draw 2, Skip, Reverse, Wild, Wild Draw 4.
- **Scoring**: Winner gets points based on cards left in opponents' hands.

## License

[MIT](LICENSE)
