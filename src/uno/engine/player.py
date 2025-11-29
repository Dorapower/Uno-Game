from dataclasses import dataclass
from typing import Any

@dataclass
class Request:
    hand: list[Any]
    hand_sizes: list[int]
    scores: list[int]
    latest_moves: list[tuple[int, Any]]
    top_card: Any | None = None


type Move = tuple[Any, ...]


class Player:
    name: str

    def __init__(self, name: str):
        self.name = name

    def play(self, request: Request) -> Move:
        """
        Player should return a Move tuple.
        The first element is the card (str) or None to draw.
        Subsequent elements are rule-specific (e.g. chosen color).
        :param request:
        :return:
        """
        raise NotImplementedError


class DrawPlayer(Player):
    def play(self, request: Request) -> Move:
        return (None,)


import random

class RandomPlayer(Player):
    def play(self, request: Request) -> Move:
        top_card = request.top_card
        if top_card is None:
            return (None,)

        # Try to find a playable card
        for card in request.hand:
            # Check for wild
            if getattr(card, 'color', '') == 'wild':
                # Pick random color
                color = random.choice(('red', 'blue', 'green', 'yellow'))
                return (card, color)
            
            # Check matching color or symbol
            if (getattr(card, 'color', '') == getattr(top_card, 'color', '') or 
                getattr(card, 'symbol', '') == getattr(top_card, 'symbol', '')):
                return (card,)
        
        # No playable card
        return (None,)
