import random
from typing import List

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
        game_state : GameState
    ) -> int:
        dice = game_state.next_roll

        while 1:
            x = int(input('\nMake your choice: '))

            if x in dice:
                return x
            else:
                print(f"{x} isn't a valid entry in {dice}.")

class JonahsGreatStrategy(Strategy):
    def choose(
        self,
        game_state : GameState
    ) -> int:
        dice = game_state.next_roll
        max_payout_casino_id = self._get_max_payout_casino_id(game_state.casinos)

        if max_payout_casino_id in dice:
            return max_payout_casino_id
        else:
            return random.choice(dice)

    def _get_max_payout_casino_id(
        self,
        casinos : List[Casino]
    ) -> int:
        max_payout = 0
        max_payout_casino_id = 0
        for casino in casinos:
            payout = casino.payouts[0]
            if payout > max_payout:
                max_payout = payout
                max_payout_casino_id = casino.id_
        
        return max_payout_casino_id


class JonahsNextGreatStrategy(Strategy):
    def choose(
        self,
        game_state : GameState
    ) -> int:

        print("=============== JONAH THE GREAT WAS HERE ===============")
        # print(game_state.casinos)
        max_payout = 0
        max_payout_casino_id = 0
        for casino in game_state.casinos:
            payout = casino.payouts[0]
            print(payout)
            if payout > max_payout:
                max_payout = payout
                max_payout_casino_id = casino.id_
        
        print("*******")
        print(max_payout)
        print(max_payout_casino_id)

        dice = game_state.next_roll

        if max_payout_casino_id in dice:
            return max_payout_casino_id
        else:
            return random.choice(dice)


strategy_registry = {
    "RandomStrategy" : RandomStrategy,
    "InputStrategy" : InputStrategy,
    "JonahsGreatStrategy" : JonahsGreatStrategy,
}