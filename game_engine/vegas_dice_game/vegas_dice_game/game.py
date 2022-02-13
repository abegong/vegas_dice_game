import datetime
import random
from typing import List

from vegas_dice_game.engine import GameEngine
from vegas_dice_game.strategy import Strategy, strategy_registry


class Game():

    engine : GameEngine
    strategies : List[Strategy]

    def __init__(
        self,
        num_players : int = 4,
        strategies = ["RandomStrategy", "RandomStrategy", "RandomStrategy", "JonahsGreatStrategy"]
    ):
        self.engine = GameEngine(num_players=len(strategies))
        self.strategies = [strategy_registry[strategy_name]() for strategy_name in strategies]


    def play_game(
        self,
        verbosity=1,
    ):
        while 1:
            next_player_id = self.engine.next_player_id
            game_state = self.engine.state

            if verbosity > 0:
                self.engine.print_state()

            if next_player_id == -1:
                break
            
            choice = self.strategies[next_player_id].choose(game_state)

            if verbosity > 0:
                print()
                print(f'> {choice}')
                print()
                print('-'*80)
                print()

            self.engine.choose_dice_location(choice)

        return self.engine._get_scores()