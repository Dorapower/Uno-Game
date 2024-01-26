from dataclasses import dataclass

from .player import Player


@dataclass(slots=True)
class Round:
    deck: list[str]
    discard: list[str]
    hands: list[list[str]]


@dataclass(slots=True)
class Context:
    players: list[Player]
    rounds: int
    current_round: Round | None = None
