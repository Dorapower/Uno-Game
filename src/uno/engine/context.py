from dataclasses import dataclass, field, InitVar
import random
from typing import NamedTuple


class Card(NamedTuple):
    color: str
    symbol: str


@dataclass(slots=True)
class Round:
    """
    A snapshot of the game state after a player played a card, and before one draws a card.
    Only be updated by rule's `step` method.
    """
    draw: list[Card] = field(default_factory=list)
    discard: list[Card] = field(default_factory=list)
    hands: list[list[Card]] = field(default_factory=list)

    turns: int = field(init=False, default=0)
    last_card: Card | None = field(init=False, default=None)
    current_player: int = field(init=False, default=0)
    active_effects: list[str] = field(init=False, default_factory=list)


@dataclass(slots=True)
class Context:
    player_count: int
    seed: InitVar[int | None] = field(default=None, kw_only=True)

    scoreboard: list[int] | None = field(init=False, default=None)
    rounds: int = field(init=False, default=0)
    current_round: Round | None = field(init=False, default=None)

    rng: random.Random = field(init=False)

    def __post_init__(self, seed: int | None):
        self.rng = random.Random(seed)
