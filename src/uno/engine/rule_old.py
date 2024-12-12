# this module is deprecated. Serves only as a reference
import random
from abc import ABC, abstractmethod
from typing import ClassVar

from .context import Context, Round


class Rule(ABC):
    """
    The rule is responsible for the game logic.
    It should contain no information related the game state and only have methods to manipulate it.
    But rules can have variants which can be passed as parameters to the constructor.
    """

    @abstractmethod
    def init_game(self, ctx: Context):
        raise NotImplementedError

    @abstractmethod
    def step(self, ctx: Context, card: str | None):
        raise NotImplementedError

    @abstractmethod
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
            draw=[color + str(number) for color in self.COLORS for number in self.NUMBERS],
            discard=[],
        )
        self._shuffle_deck(ctx)
        for _ in range(self.HAND_SIZE):
            for idx in range(ctx.player_count):
                self._draw_card(ctx, idx)

    def _shuffle_deck(self, ctx: Context):
        self.rng.shuffle(ctx.current_round.draw)

    def _refill_deck(self, ctx: Context):
        round_ = ctx.current_round
        round_.draw.extend(round_.discard)
        self._shuffle_deck(ctx)
        round_.discard.clear()

    def _draw_card(self, ctx: Context, player: int):
        round_ = ctx.current_round
        if len(round_.draw) == 0:
            self._refill_deck(ctx)
            if len(round_.draw) == 0:
                raise RuntimeError('No cards left in deck')
        round_.hands[player].append(round_.draw.pop())

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


class StandardRule(Rule):
    """
    Standard UNO rule, based on instruction sheet of 2008 version of the game. The first player to reach 500 points wins.
    """

    COLORS: ClassVar[tuple[str, ...]] = ('red', 'blue', 'green', 'yellow')
    NUMBERS: ClassVar[tuple[int, ...]] = tuple(range(8))
    ACTIONS: ClassVar[tuple[str, ...]] = ('draw_2', 'reverse', 'skip', 'wild', 'wild_draw_4')
    ACTION_VALUES: ClassVar[tuple[int, ...]] = (20, 20, 20, 50, 50)
    TARGET_SCORE: ClassVar[int] = 500
    HAND_SIZE: ClassVar[int] = 7

    def init_game(self, ctx: Context):
        """
        Initialize the context on the start of the game.

        :param ctx:
        :return:
        """
        ctx.current_round.draw = [f"{color}_{number}" for color in self.COLORS for number in self.NUMBERS]
        self._shuffle_deck(ctx)
        for _ in range(self.HAND_SIZE):
            for idx in range(ctx.player_count):
                self._draw_card(ctx, idx)

    def _shuffle_deck(self, ctx: Context):
        """
        shuffle the deck so cards are distributed randomly
        :param ctx:
        :return:
        """
        ctx.rng.shuffle(ctx.current_round.draw)

    def _refill_deck(self, ctx: Context):
        """
        called when the deck is empty, refill it with the discard pile
        :param ctx:
        :return:
        """
        assert len(ctx.current_round.draw) == 0

        round_ = ctx.current_round
        round_.draw.extend(round_.discard)
        top_card = round_.draw.pop()  # the top card is left in the discard
        round_.discard = [top_card]

        self._shuffle_deck(ctx)

    def _draw_card(self, ctx: Context, player: int) -> str | None:
        """
        player decided to draw a card. have no effect if no card left
        :param ctx:
        :param player: the player to draw
        :return: the card drawn. None if no card left
        """
        round_ = ctx.current_round
        if len(round_.draw) == 0:  # fill the deck if necessary
            self._refill_deck(ctx)
        if len(round_.draw) == 0:  # no card left in either deck or discard
            return None

        card = round_.draw.pop()
        round_.hands[player].append(card)
        return card

    def step(self, ctx: Context, card: str | None) -> tuple[int, str]:
        """
        compatible version of the step function.
        :param ctx:
        :param card: card played by the current player, None if the player decided to draw a card
        :return: current player, card played
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

    def _step(self, ctx: Context, action: str):
        """
        main logic of the game. handles player's last action and wait for the next one.
        :param ctx:
        :param action: either the card played or draw
        :return:
        """
        assert ctx.current_round is not None
        assert not self.is_over(ctx)
        round_ = ctx.current_round

        if action == 'draw':
            self._draw_card(ctx, round_.current_player)
        else:
            round_.current_card = action
            round_.discard.append(action)
            round_.hands[round_.current_player].remove(action)

        round_.turns += 1