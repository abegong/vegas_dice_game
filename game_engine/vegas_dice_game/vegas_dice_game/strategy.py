import random

from vegas_dice_game.engine import GameState

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

class InputStrategy():
    def choose(
        self,
        game_state : GameState
    ) -> int:
        dice = game_state.next_roll

        while 1:
            x = int(input('\nMake your choice: '))

            if x in dice:
                return x
            else:
                print(f"{x} isn't a valid entry in {dice}.")
