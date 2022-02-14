from dataclasses import asdict
import json
import random

from vegas_dice_game.engine import GameState, Casino

class Strategy():
    def choose(
        game_state : GameState
    ) -> int:
        raise NotImplementedError

class RandomStrategy(Strategy):
    def choose(
        self,
        game_state : GameState
    ) -> int:
        dice = game_state.next_roll
        return random.choice(dice)

class InputStrategy(Strategy):
    def choose(
        self,
        game_state : GameState,
        log_file : str = "InputStrategy.log",
    ) -> int:
        dice = game_state.next_roll

        while 1:
            x = int(input('\nMake your choice: '))

            if x in dice:
                break
            else:
                print(f"{x} isn't a valid entry in {dice}.")

        with open(log_file, "a") as myfile:
            myfile.write(str(x) + " " + json.dumps(asdict(game_state))+"\n")

        return x