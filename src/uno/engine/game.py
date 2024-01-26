from .player import Player
from .rule import Rule
from .context import Context, Round


class Game:
    context: Context
    rule: Rule
    history: list

    def __init__(self, rule: Rule, n_players: int = 4):
        self.context = Context([Player()] * n_players, 0)
        self.history = []

        self.rule = rule

    def start(self):
        while not self.rule.is_over(self.context):
            self.history.append(self.rule.step(self.context))
