from typing import NamedTuple
from collections.abc import Callable

from .context import Context, Round


class Rule(NamedTuple):
    init_game: Callable[[Context], ...]  # initialize the context on the start of the game
    step: Callable[[Context, str], ...]  # handle the last action and wait for the next one
    is_over: Callable[[Context], bool]  # check if the game is finished
