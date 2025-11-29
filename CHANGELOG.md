# Changelog

All notable changes to this project will be documented in this file.

## [0.2.0a1] - 2025-11-30

### Added
- **Command-Line Interface**: Added `src/cli.py` for interactive play against bots.
- **AI Opponents**: Implemented `RandomPlayer` in `src/uno/engine/player.py` as a basic bot.
- **Testing**: Added comprehensive `pytest` suite in `tests/` covering rules, scoring, and player logic.
- **Type Hints**: Enhanced type safety across the codebase, specifically for `Move` and `Request` objects.

### Changed
- **Engine Refactoring**: Updated `Player.play` to return a `Move` tuple `(card, metadata)` to support complex moves (e.g., Wild card color selection).
- **Rule Logic**:
    - Fixed `init_game` and `init_round` to correctly initialize game state and discard pile.
    - Implemented `update_score` to calculate scores at the end of a round.
    - Improved `step` function to handle round transitions and move validation.
    - Ensured the starting card of a round is never a Wild card.
- **Configuration**: Updated `pyproject.toml` to require Python 3.11+ and include `pytest` as a dependency.

### Fixed
- **Game Initialization**: Resolved `AttributeError` issues caused by improper `current_round` initialization.
- **Wild Card Handling**: Fixed issues where Wild cards were auto-playing as 'red' or causing crashes.
- **Round Management**: Corrected logic for detecting round end and starting new rounds.
