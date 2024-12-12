"""
Standard UNO rule, based on instruction sheet of 2008 version of the game
The first player to reach 500 points wins
"""

from ..engine.rule import Rule
from ..engine.context import Context

COLORS: tuple[str, ...] = ('red', 'blue', 'green', 'yellow')
NUMBERS: tuple[int, ...] = tuple(range(8))
ACTIONS: tuple[str, ...] = ('draw_2', 'reverse', 'skip', 'wild', 'wild_draw_4')
VALUES: dict[str, int] = {'draw_2': 20, 'reverse': 20, 'skip': 20, 'wild': 50, 'wild_draw_4': 50}
HAND_SIZE: int = 7

def init_game(ctx: Context):
    """
    Initialize the context on the start of the game
    :param ctx:
    :return:
    """
    pass

def is_over(ctx: Context):
    """
    check if the game is over
    :param ctx:
    :return:
    """
    return False

def step(ctx: Context, card: str | None):
    """
    main logic of the game. handle the last action and wait for the next one
    :param ctx:
    :param card: card played by the current player, None if the player decided to draw a card
    :return:
    """
    pass

rule: Rule = Rule(init_game, step, is_over)