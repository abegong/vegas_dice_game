import random
from typing import Dict, List
from dataclasses import dataclass

from vegas_dice_game.names import generate_random_name

@dataclass
class Player():
    id_ : int
    name : str
    dice_remaining : int
    total_cash : int = 0

    def __str__(self):
        return f'{self.id_}: {self.name : >13} (${self.total_cash}) : {self.dice_remaining} dice remaining'

@dataclass
class Casino():
    id_ : int
    payouts : List[int]
    placed_dice : List[int]

    def __str__(self):
        string = f'{self.id_}: '
        for count in self.placed_dice:
            string += f'{count : >3}'
        string += ' | '
        
        for payout in self.payouts:
            string += f' ${payout} '

        return string

@dataclass
class GameState():
    round_number : int
    players : List[Player]
    casinos : List[Casino]
    next_player_id : int
    next_roll : List[int]

class GameEngine():
    round_number : int

    players : List[Player]
    casinos : List[Casino]

    next_player_id : int
    next_roll : List[int]

    def __init__(
        self,
        num_players = 4,
        num_casinos = 6,
        num_dice = 8,
    ):
        self.players = self._create_players(
            num_players=num_players,
            num_dice=num_dice,
        )
        self.casinos = self._create_casinos(
            num_casinos=num_casinos,
            num_players=num_players,
        )
        self.round_number = 0
        self.next_player_id = 0

        self._get_next_roll()
        
    def _create_players(
        self,
        num_players,
        num_dice,
    ) -> List[Player]:
        return [
            Player(
                id_ = i,
                dice_remaining = num_dice,
                total_cash = 0,
                name = generate_random_name(),
            )
            for i in range(num_players)
        ]
    
    def _create_casinos(
        self,
        num_casinos,
        num_players,
    ) -> List[Casino]:
        return [
            Casino(
                id_ = i,
                payouts = self._generate_payouts(),
                placed_dice = [0 for i in range(num_players)]
            )
            for i in range(num_casinos)
        ]

    def _get_next_roll(
        self,
    ) -> List[int]:
        dice = [random.randint(0, 5) for i in range(self.players[self.next_player_id].dice_remaining)]
        dice.sort()
        self.next_roll = dice

    def choose_dice_location(
        self,
        casino_id,
    ) -> int:
        dice_count = sum([1 for i in self.next_roll if i == casino_id])

        self.players[self.next_player_id].dice_remaining -= dice_count
        self.casinos[casino_id].placed_dice[self.next_player_id] += dice_count

        self._get_next_player()
        self._get_next_roll()

    def _any_players_with_dice_remain(self) -> bool:
        players_remain = False
        for p in self.players:
            if p.dice_remaining > 0:
                players_remain = True
                break

        return players_remain

    def _get_next_player(self):
        """Get the id of the next player with nonzero dice remaining.
        
        If no players remain, return -1
        """
        if self._any_players_with_dice_remain() == False:
            self.next_player_id = -1
            return

        next_player_id = self.next_player_id
        while 1:
            next_player_id = (next_player_id + 1) % len(self.players)
            if self.players[next_player_id].dice_remaining > 0:
                break
        
        self.next_player_id = next_player_id

    def _generate_payouts(
        self,
        min_payout : int = 50,
        possible_payouts : List[int] = [10, 20, 30, 40, 50, 60, 70, 80, 90],
    ) -> List[int]:
        payouts = []

        while sum(payouts) < min_payout:
            payouts.append( random.choice(possible_payouts) )
        payouts.sort(reverse=True)

        return payouts

    @staticmethod
    def _score_casino(
        casino : Casino
    ) -> List[int]:
        winning_player_id_sequence = []
        placed_dice = [i for i in casino.placed_dice]

        while placed_dice != [0 for i in placed_dice]:
            max_dice = max(placed_dice)
            number_equal_to_max = sum([1 for i in placed_dice if i == max_dice])

            for i, j in enumerate(placed_dice):
                if j == max_dice:
                    # If there's an untied winner, add their id to the queue of winners
                    if number_equal_to_max == 1:
                        winning_player_id_sequence.append(i)

                    #Either way, remove the dice counts from placed_dice
                    placed_dice[i] = 0
            
        player_payouts = [0 for i in casino.placed_dice]
        for i, player_id in enumerate(winning_player_id_sequence):
            try:
                player_payouts[player_id] += casino.payouts[i]
            except IndexError:
                break

        return player_payouts

    def _get_scores(
        self
    ) -> List[int]:
        player_payouts = [0 for i in self.players]

        for casino in self.casinos:
            new_player_payouts = self._score_casino(casino)
            for i, p in enumerate(new_player_payouts):
                player_payouts[i] += p
        
        return player_payouts

    @property
    def state(self):
        return GameState(
            round_number=self.round_number,
            players=self.players,
            casinos=self.casinos,
            next_player_id=self.next_player_id,
            next_roll=self.next_roll,
        )

    def print_state(self):
        print("=============== Players ===============")
        for player in self.players:
            print(player)
        print()

        print("=============== Casinos ===============")
        for casino in self.casinos:
            print(casino)
        print()

        if self.next_player_id == -1:
            print(f'All players have placed all their dice. The game is over.')
            print(self._get_scores())

        else:
            print(f'{self.players[self.next_player_id].name} is next, with this roll:')
            print("  "+(" ".join([str(i) for i in self.next_roll]) ))