from dataclasses import dataclass


@dataclass
class Request:
    hand: list[str]
    hand_sizes: list[int]
    scores: list[int]
    latest_moves: list[tuple[int, str]]


class Player:
    name: str

    def __init__(self, name: str):
        self.name = name

    def play(self, request: Request) -> str | None:
        """
        Player should return a string of the card to play, or None to draw
        :param request:
        :return:
        """
        raise NotImplementedError


class DrawPlayer(Player):
    def play(self, request: Request) -> str | None:
        return None
