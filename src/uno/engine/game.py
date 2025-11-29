import logging
import datetime
from typing import Any

from .player import Player, Request, DrawPlayer
from .rule import Rule
from .context import Context

logger = logging.getLogger(__name__)


class Game:
    """
    Root class, calling rule to play the game, interacting with players and keeping track of the game history
    """
    context: Context
    rule: Rule
    players: list[Player]

    history: list[Any]

    def __init__(self, rule: Rule, n_players: int = 4, seed: int | None = None):
        self.context = Context(n_players, seed=seed)
        self.players = [DrawPlayer(str(i)) for i in range(n_players)]
        self.history = []

        self.rule = rule

    def build_request(self, idx: int):
        hand = self.context.current_round.hands[idx]
        hand_sizes = list(map(len, self.context.current_round.hands))
        scores = self.context.scoreboard
        latest_move = self.history  # survival is more important than efficiency
        
        # Get top card (last_card) from current round
        top_card = None
        if self.context.current_round:
            top_card = self.context.current_round.last_card

        return Request(hand, hand_sizes, scores, latest_move, top_card)

    def start(self):
        """
        Main game loop, on each step, the rule is called to update the context and the current players are asked to play
        :return:
        """
        logger.info("Starting game")
        self.rule.init_game(self.context)
        while not self.rule.is_over(self.context):
            cur_player = self.context.current_round.current_player
            request = self.build_request(cur_player)
            move = self.players[cur_player].play(request)
            self.history.append(self.rule.step(self.context, move))
            logger.info(f"Player {cur_player} played {move}")
