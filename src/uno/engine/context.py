from dataclasses import dataclass

from .player import Player


@dataclass(slots=True)
class Round:
    """
    A snapshot of the game state after a player played a card, and before one draws a card.
    Only be updated by rule's `step` method.
    """
    deck: list[str]
    discard: list[str]
    hands: list[list[str]]
    turns: int = 0
    last_card: str | None = None
    current_effect: str | None = None
    current_player: int = 0
    current_card: str | None = None


@dataclass(slots=True)
class Context:
    player_count: int
    scoreboard: list[int] | None = None
    rounds: int = 0
    current_round: Round | None = None
