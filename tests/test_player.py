
import pytest
import pytest
from uno.engine.player import RandomPlayer, Request
from uno.engine.context import Card

@pytest.fixture
def player():
    return RandomPlayer("Bot")

def test_random_player_draws_when_no_playable(player):
    hand = [Card('red', 1)]
    top_card = Card('blue', 5)
    req = Request(hand=hand, hand_sizes=[], scores=[], latest_moves=[], top_card=top_card)
    
    move = player.play(req)
    assert move == (None,)

def test_random_player_plays_matching_color(player):
    hand = [Card('red', 1), Card('blue', 2)]
    top_card = Card('red', 5)
    req = Request(hand=hand, hand_sizes=[], scores=[], latest_moves=[], top_card=top_card)
    
    move = player.play(req)
    assert move[0] == Card('red', 1)

def test_random_player_plays_matching_symbol(player):
    hand = [Card('red', 1), Card('blue', 5)]
    top_card = Card('green', 5)
    req = Request(hand=hand, hand_sizes=[], scores=[], latest_moves=[], top_card=top_card)
    
    move = player.play(req)
    assert move[0] == Card('blue', 5)

def test_random_player_plays_wild(player):
    hand = [Card('wild', 'wild')]
    top_card = Card('green', 5)
    req = Request(hand=hand, hand_sizes=[], scores=[], latest_moves=[], top_card=top_card)
    
    move = player.play(req)
    assert move[0].color == 'wild'
    assert len(move) == 2
    assert move[1] in ('red', 'blue', 'green', 'yellow')
