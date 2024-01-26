from dataclasses import dataclass


@dataclass
class Request:
    hand: list[str]
    hand_sizes: list[int]
    scores: list[int]
    latest_moves: list[tuple[int, str]]
    order: str


class Player:
    name: str

    def __init__(self, name: str):
        self.name = name

    def act(self, request: Request) -> str:
        """
        Player should return a string of the card to play
        :param request:
        :return:
        """
        raise NotImplementedError

