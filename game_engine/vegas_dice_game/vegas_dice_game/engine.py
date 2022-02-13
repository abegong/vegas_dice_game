import datetime
import random
from typing import List

from vegas_dice_game.game import GameEngine
from vegas_dice_game.strategy import Strategy, RandomStrategy


class Game():

    engine : GameEngine
    strategies : List[Strategy]

    def __init__(
        self,
        num_players : int = 4,
    ):
        self.engine = GameEngine()#num_players=num_players)
        self.strategies = [RandomStrategy() for i in range(num_players)]

    def play_game(
        self
    ):
        for i in range(20):
            next_player_id = self.engine.next_player_id
            game_state = self.engine.state

            self.engine.print_state()
            # print(next_player_id)

            if next_player_id == -1:
                break
            
            choice = self.strategies[next_player_id].choose(game_state)

            print()
            print(f'> {choice}')
            print()
            print('-'*80)
            print()

            self.engine.choose_dice_location(choice)