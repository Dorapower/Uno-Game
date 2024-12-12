import logging

from uno.engine.game import Game
from uno.engine.rule_old import ExampleRule
from uno.rules.base import rule


def main():
    game = Game(rule=rule, n_players=2)
    game.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
