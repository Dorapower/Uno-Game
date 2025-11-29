"""
Standard UNO rule, based on instruction sheet of 2008 version of the game
The first player to reach 500 points wins
"""
import random
from functools import cache

from ..engine.rule import Rule
from ..engine.context import Context, Round, Card

COLORS: tuple[str, ...] = ('red', 'blue', 'green', 'yellow', 'wild')
SYMBOLS: tuple[int, ...] = tuple(range(8))
ACTIONS: tuple[str, ...] = ('draw_2', 'reverse', 'skip', 'wild', 'wild_draw_4')
ACTION_VALUES: dict[str, int] = {'draw_2': 20, 'reverse': 20, 'skip': 20, 'wild': 50, 'wild_draw_4': 50}
HAND_SIZE: int = 7


def build_deck() -> list[Card]:
    """
    build a new deck and return each time called
    :return: new deck in order.
    """
    colors = COLORS[:-1]
    wild = colors[-1]
    non_wild_types = SYMBOLS + ACTIONS[:-2]
    wild_types = ACTIONS[-2:]

    return (
        [Card(color, symbol) for color in colors for symbol in non_wild_types] +
        [Card(wild, symbol) for symbol in wild_types]
    )


def init_round(ctx: Context):
    """
    initialize a new round
    :param ctx:
    :return:
    """
    ctx.rounds += 1

    # collect cards
    draw = build_deck()
    shuffle(ctx, draw)

    # deal cards to players
    hands = [[] for _ in range(ctx.player_count)]
    for _ in range(HAND_SIZE):
        for idx in range(ctx.player_count):
            hands[idx].append(draw.pop())

    # discard pile
    while draw[0].color == 'wild':
        shuffle(ctx, draw)

    discard = [draw.pop(0)]

    # finish building
    ctx.current_round = Round(
        draw= draw,
        discard = discard,
        hands = hands,
    )
    ctx.current_round.last_card = discard[-1]


def round_is_over(round_: Round) -> bool:
    """
    check if the round is over based on the hands
    :param round_:
    :return: True if the round is over
    """
    return any(len(hand) == 0 for hand in round_.hands)


def init_game(ctx: Context):
    """
    Initialize the context on the start of the game
    :param ctx:
    :return:
    """
    if not 2 <= ctx.player_count <= 10:
        raise RuntimeError('Player count must be between 2 and 10')
    ctx.scoreboard = [0] * ctx.player_count
    ctx.rounds = -1
    init_round(ctx)


def game_is_over(ctx: Context):
    """
    check if the game is over based on the scoreboard
    :param ctx:
    :return: True if the game is over
    """
    return any(score >= 500 for score in ctx.scoreboard)


def shuffle(ctx: Context, pile: list[Card]):
    """
    shuffle the provided pile so cards are arranged randomly
    :param ctx:
    :param pile: a pile of cards to shuffle
    :return:
    """
    ctx.rng.shuffle(pile)


def replenish_draw(ctx: Context):
    """
    called when the draw pile is empty, refill it with the discard pile.
    * If there is no available cards, do nothing
    :param ctx:
    :return:
    """
    assert len(ctx.current_round.draw) == 0

    round_ = ctx.current_round
    round_.draw.extend(round_.discard)
    last_card = round_.draw.pop()  # the top card is left in the discard
    round_.discard = [last_card]

    shuffle(ctx, round_.draw)


def draw_card(ctx: Context, player: int) -> Card | None:
    """
    player decided to draw a card. have no effect if no card left
    :param ctx:
    :param player: the player to draw
    :return: the card drawn. None if no card is drawn
    """
    round_ = ctx.current_round
    if len(round_.draw) == 0:  # fill the deck if necessary
        replenish_draw(ctx)
    if len(round_.draw) == 0:  # no card left in either deck or discard
        return None

    card = round_.draw.pop()
    round_.hands[player].append(card)
    return card


def is_playable(ctx: Context, card: Card) -> bool:
    """
    check if the card can be played
    :param ctx:
    :param card: the card to check
    :return: True if the card can be played
    """
    round_ = ctx.current_round
    # If there are blocking effects, no card is playable (must draw/resolve effect)
    blocking_effects = {'skip', 'draw_2', 'wild_draw_4'}
    if any(eff in round_.active_effects for eff in blocking_effects):
        return False

    last_card = round_.last_card
    # Wild cards are always playable
    if card.color == 'wild':
        return True
    # Otherwise match color or symbol
    return card.color == last_card.color or card.symbol == last_card.symbol


def update_score(ctx: Context):
    """
    Calculate scores at the end of a round and update scoreboard.
    Winner gets sum of values of cards in other players' hands.
    """
    round_ = ctx.current_round
    if round_ is None:
        return

    winner_idx = -1
    for idx, hand in enumerate(round_.hands):
        if len(hand) == 0:
            winner_idx = idx
            break
    
    if winner_idx != -1:
        points = 0
        for hand in round_.hands:
            for card in hand:
                if isinstance(card.symbol, int):
                    points += card.symbol
                elif str(card.symbol) in ACTION_VALUES:
                    points += ACTION_VALUES[str(card.symbol)]
        
        ctx.scoreboard[winner_idx] += points


def step(ctx: Context, move: tuple):
    """
    main logic of the game. handle the last action and wait for the next one
    :param ctx:
    :param move: tuple where first element is Card or None (to draw), second is color (if wild)
    :return:
    """
    round_ = ctx.current_round
    
    if round_ is None or round_is_over(round_):
        if round_ is not None:
            update_score(ctx)
        init_round(ctx)
        return move

    effects = round_.active_effects
    
    card = move[0]
    color_chosen = move[1] if len(move) > 1 else None

    # Validate move
    if card is not None and not is_playable(ctx, card):
        # Invalid move, treat as draw/pass
        card = None

    # round is not over
    round_.turns += 1

    if card is None:  # player decided to not play (draw)
        match effects:
            case _ if 'skip' in effects:
                effects.remove('skip')
            case _ if 'draw_2' in effects:
                for _ in range(2):
                    _ = draw_card(ctx, round_.current_player)
                effects.remove('draw_2')
            case _ if 'wild_draw_4' in effects:
                for _ in range(4):
                    _ = draw_card(ctx, round_.current_player)
                effects.remove('wild_draw_4')
            case _:
                # player decided to draw
                # newly drawn card will be played if possible
                new_card = draw_card(ctx, round_.current_player)
                if new_card and is_playable(ctx, new_card):
                    # Auto-play drawn card if playable
                    # If it's wild, we default to 'red' since we can't ask player again in this flow
                    # This is a limitation of the current synchronous engine
                    card = new_card
                    if card.color == 'wild':
                        color_chosen = 'red' 

    if card is not None:  # player decided to play a card (or auto-played)
        # Update last_card for playability checks
        if card.color == 'wild':
            if color_chosen not in COLORS[:-1]: # Ensure valid color
                 color_chosen = 'red'
            round_.last_card = Card(color_chosen, card.symbol)
        else:
            round_.last_card = card
            
        round_.discard.append(card)
        round_.hands[round_.current_player].remove(card)
        
        match card.symbol:  # update active effects
            case 'reverse' if 'reverse' in effects:
                effects.remove('reverse')
            case symbol if symbol in ACTIONS:
                effects.append(symbol)

    # update current player
    if 'reverse' in effects:
        round_.current_player = (round_.current_player - 1) % ctx.player_count
    else:
        round_.current_player = (round_.current_player + 1) % ctx.player_count
        
    final_move = (card,)
    if card and card.color == 'wild':
        final_move = (card, color_chosen)
    return final_move


rule: Rule = Rule(init_game, step, game_is_over)