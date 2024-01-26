import random

from .context import Context


class Rule:
    def init_deck(self, ctx: Context):
        raise NotImplementedError

    def step(self, ctx: Context):
        raise NotImplementedError

    def is_over(self, ctx: Context):
        raise NotImplementedError


class ExampleRule(Rule):
    cards: tuple[str] = ('red', 'blue', 'green', 'yellow', 'wild', 'wild_draw_four')

    def init_deck(self, ctx: Context):
        return [(color, number) for color in self.cards for number in range(10)]

    def step(self, ctx: Context):
        assert ctx.current_round is not None

        round_ = ctx.current_round
        if len(round_.deck) == 0:
            round_.deck.extend(round_.discard)
            random.shuffle(round_.deck)
            round_.discard.clear()
        return round_.deck.pop()

    def is_over(self, scoreboard):
        return any(score >= 500 for score in scoreboard)

    @staticmethod
    def is_round_over(ctx: Context):
        return any(len(hand) == 0 for hand in ctx.current_round.hands)
