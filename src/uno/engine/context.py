from dataclasses import dataclass, field
import random


@dataclass(slots=True)
class Round:
    """
    A snapshot of the game state after a player played a card, and before one draws a card.
    Only be updated by rule's `step` method.
    """
    deck: list[str]
    discard: list[str]
    hands: list[list[str]]
    turns: int = field(init=False, default=0)
    last_card: str | None = None
    current_effect: str | None = None
    current_player: int = 0
    current_card: str | None = None


@dataclass(slots=True)
class Context:
    player_count: int
    seed: int | None = field(default=None, repr=False, kw_only=True)

    scoreboard: list[int] = field(init=False)
    rounds: int = field(init=False, default=0)
    current_round: Round = field(init=False)
    rng: random.Random = field(init=False)

    def __post_init__(self):
        self.scoreboard = [0] * self.player_count
        self.current_round = Round(
            deck=[],
            discard=[],
            hands=[[] for _ in range(self.player_count)],
        )
        self.rng = random.Random(self.seed)
