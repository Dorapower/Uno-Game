import logging

from uno.engine.game import Game
from uno.engine.rule import ExampleRule
from uno.engine.player import DrawPlayer


def main():
    game = Game(rule=ExampleRule(), n_players=2)
    game.start()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
