from pydantic.dataclasses import dataclass
import random


def make_player():
    id = 1
    return id


def get_player(id):
    pass


def get_all_players():
    pass


def update_rating():
    pass


@dataclass
class Player:
    id: int
    name: str
    rating: float
    rd: float


def play_game(p1: Player, p2: Player) -> int:
    # TODO: determin winner using the rating logic and some randomness
    result = random.randint(0, 2) / 2
    return result
