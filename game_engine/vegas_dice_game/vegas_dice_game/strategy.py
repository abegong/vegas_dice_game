import random

from vegas_dice_game.game import GameState

class Strategy():
    def choose(
        game_state : GameState
    ) -> int:
        raise NotImplementedError

class RandomStrategy():
    def choose(
        self,
        game_state : GameState
    ) -> int:
        dice = game_state.next_roll
        return random.choice(dice)