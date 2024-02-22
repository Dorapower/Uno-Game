import random
from typing import ClassVar

from .context import Context, Round


class Rule:
    """
    The rule is responsible for the game logic.
    It should contain no information related the game state and only have methods to manipulate it.
    But rules can have variants which can be passed as parameters to the constructor.
    """
    def init_game(self, ctx: Context):
        raise NotImplementedError

    def step(self, ctx: Context, card: str | None):
        raise NotImplementedError

    def is_over(self, ctx: Context):
        raise NotImplementedError


class ExampleRule(Rule):
    """
    Similar to UNO but simplified to have no action cards etc.
    """
    COLORS: ClassVar[tuple[str, ...]] = ('red', 'blue', 'green', 'yellow')
    NUMBERS: ClassVar[tuple[int, ...]] = tuple(range(8))
    HAND_SIZE: ClassVar[int] = 7

    rng: random.Random

    def __init__(self, seed: int | None = None):
        self.rng = random.Random(seed)

    def init_game(self, ctx: Context):
        ctx.scoreboard = [0 for _ in range(ctx.player_count)]
        ctx.current_round = Round(
            hands=[[] for _ in range(ctx.player_count)],
            deck=[color + str(number) for color in self.COLORS for number in self.NUMBERS],
            discard=[],
        )
        self._shuffle_deck(ctx)
        for _ in range(self.HAND_SIZE):
            for idx in range(ctx.player_count):
                self._draw_card(ctx, idx)

    def _shuffle_deck(self, ctx: Context):
        self.rng.shuffle(ctx.current_round.deck)

    def _refill_deck(self, ctx: Context):
        round_ = ctx.current_round
        round_.deck.extend(round_.discard)
        self._shuffle_deck(ctx)
        round_.discard.clear()

    def _draw_card(self, ctx: Context, player: int):
        round_ = ctx.current_round
        if len(round_.deck) == 0:
            self._refill_deck(ctx)
            if len(round_.deck) == 0:
                raise RuntimeError('No cards left in deck')
        round_.hands[player].append(round_.deck.pop())

    def step(self, ctx: Context, card: str | None) -> tuple[int, str]:
        """
        main logic of the game. handle the last action and wait for the next one.
        :param ctx: context of the game
        :param card: card played by the current player, None if the player decided to draw a card
        :return: cards played
        """
        assert ctx.current_round is not None
        assert not self.is_over(ctx)
        round_ = ctx.current_round

        if card is None:
            self._draw_card(ctx, round_.current_player)
        else:
            round_.current_card = card
            round_.discard.append(card)
            round_.hands[round_.current_player].remove(card)

        round_.turns += 1
        round_.current_player = (round_.current_player + 1) % ctx.player_count
        return round_.current_player, card

    def is_over(self, ctx: Context):
        return any(len(hand) == 0 for hand in ctx.current_round.hands)
