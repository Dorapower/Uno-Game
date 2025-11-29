
import sys
import logging
from uno.engine.game import Game
from uno.engine.player import Player, Request, Move
from uno.rules.base import rule as standard_rule

from uno.engine.player import RandomPlayer

# Configure logging to show game events
logging.basicConfig(level=logging.INFO, format='%(message)s')

class HumanPlayer(Player):
    def play(self, request: Request) -> Move:
        print(f"\n--- Player {self.name}'s Turn ---")
        print(f"Top Card: {request.top_card}")
        print("Your Hand:")
        for idx, card in enumerate(request.hand):
            print(f"  {idx}: {card}")
        
        while True:
            choice = input("Enter card index to play, or 'd' to draw: ").strip().lower()
            if choice == 'd':
                return (None,)
            
            try:
                idx = int(choice)
                if 0 <= idx < len(request.hand):
                    card = request.hand[idx]
                    # Check if wild to ask for color
                    # Note: We are checking 'wild' string on the card object. 
                    # Assuming card has .color attribute or is accessible.
                    # Since we use Any in Request, we assume it's the Card namedtuple.
                    if getattr(card, 'color', '') == 'wild':
                        while True:
                            color = input("Choose color (red, blue, green, yellow): ").strip().lower()
                            if color in ('red', 'blue', 'green', 'yellow'):
                                return (card, color)
                            print("Invalid color.")
                    
                    # Basic client-side validation
                    top_card = request.top_card
                    if top_card and getattr(card, 'color', '') != 'wild':
                         # Check if matches top card
                         if card.color != top_card.color and card.symbol != top_card.symbol:
                             print(f"Invalid move! Card {card} does not match {top_card}")
                             continue

                    return (card,)
                else:
                    print("Invalid index.")
            except ValueError:
                print("Invalid input.")

def main():
    print("Welcome to UNO!")
    try:
        n_players = int(input("How many players (2-10)? ") or "4")
    except ValueError:
        n_players = 4
        
    game = Game(standard_rule, n_players=n_players)
    # Use RandomPlayer for bots
    game.players = [RandomPlayer(str(i)) for i in range(n_players)]
    
    # Replace first player with Human
    game.players[0] = HumanPlayer("Human")
    
    # Run game
    try:
        game.start()
    except KeyboardInterrupt:
        print("\nGame aborted.")

if __name__ == "__main__":
    main()
