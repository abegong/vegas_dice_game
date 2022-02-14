import json
import pandas as pd
from numpy import array, argmax
from sklearn.linear_model import LogisticRegression

from vegas_dice_game.engine import GameState, Casino, Player
from vegas_dice_game.strategy.base import Strategy

class MLBasedStrategy(Strategy):

    def _load_training_data(self):
        training_data = pd.DataFrame()
        filenames = [
            "../../model/InputStrategy-20220213-A.log",
            "../../model/InputStrategy-20220213-B.log",
            "../../model/InputStrategy-20220213-C.log",
        ]
        for filename in filenames:
            df = self._load_file_and_create_feature_data_frame(filename)
            training_data = pd.concat([training_data, df])

        self.training_data = training_data

    def _load_file_and_create_feature_data_frame(
        self,
        filename,
    ) -> pd.DataFrame:
        raise NotImplementedError

    @staticmethod
    def _get_choice_and_game_state_from_line(line):
        choice_, game_state = line.split(' ', 1)

        game_state_json = json.loads(game_state)
        game_state = game_state_json
        game_state["casinos"] = [Casino(**c) for c in game_state["casinos"]]
        game_state["players"] = [Player(**p) for p in game_state["players"]]
        game_state = GameState(**game_state)
        
        return choice_, game_state

    @staticmethod
    def _calc_feature_total_other_dice_remaining(
        game_state,
        my_id,
    ):
        return sum([game_state.players[id_].dice_remaining for id_ in range(len(game_state.players)) if not id_ == my_id ])

    @staticmethod
    def _calc_feature_my_dice_lead(
        casino,
        my_id,
        num_players,
    ):
        my_dice = casino.placed_dice[my_id]
        max_other_dice = max([casino.placed_dice[id_] for id_ in range(num_players) if not id_ == my_id ])
        return my_dice - max_other_dice

    @classmethod
    def _get_features_from_game_state(
        cls,
        game_state
    ):
        my_id = game_state.next_player_id

        features = {
            "my_dice_remaining" : game_state.players[my_id].dice_remaining,
            "total_other_dice_remaining" : cls._calc_feature_total_other_dice_remaining(game_state, my_id),
        }
        # print(general_features)

        for casino in game_state.casinos:
            casino_id = casino.id_
            casino_level_features = {
                f"casino_{casino_id}_num_dice_to_be_placed" : sum([1 for i in game_state.next_roll if i == casino_id]),
                f"casino_{casino_id}_my_total_dice" : casino.placed_dice[my_id],
                f"casino_{casino_id}_total_other_dice" : sum([casino.placed_dice[id_] for id_ in range(len(game_state.players)) if not id_ == my_id]),
                f"casino_{casino_id}_total_players" : sum([casino.placed_dice[id_] > 0 for id_ in range(len(game_state.players))]),
                f"casino_{casino_id}_my_dice_lead" : cls._calc_feature_my_dice_lead(casino, my_id, len(game_state.players)),
                f"casino_{casino_id}_max_payoff" : casino.payouts[0],
                f"casino_{casino_id}_num_payoffs" : len(casino.payouts),
                f"casino_{casino_id}_total_payoff" : sum(casino.payouts),
            }
        #     print(casino_level_features)

            features = {**features, **casino_level_features}

        return features


class MultinomialLogisticCasinoClassifierStrategy(MLBasedStrategy):

    def choose(
        self,
        game_state : GameState
    ) -> int:
        features = self._get_features_from_game_state(game_state)
        feature_vector = array([i for i in features.values()]).reshape(1, -1)
        y_hat = self.model.predict_proba(feature_vector)

        while 1:
            max_prob_casino_id = argmax(y_hat)

            dice = game_state.next_roll
            if max_prob_casino_id in dice:
                return max_prob_casino_id
            else:
                y_hat[0, max_prob_casino_id] = -1


    x_vars = [
        'my_dice_remaining', 'total_other_dice_remaining',
        'casino_0_num_dice_to_be_placed', 'casino_0_my_total_dice',
        'casino_0_total_other_dice', 'casino_0_total_players',
        'casino_0_my_dice_lead', 'casino_0_max_payoff', 'casino_0_num_payoffs',
        'casino_0_total_payoff', 'casino_1_num_dice_to_be_placed',
        'casino_1_my_total_dice', 'casino_1_total_other_dice',
        'casino_1_total_players', 'casino_1_my_dice_lead',
        'casino_1_max_payoff', 'casino_1_num_payoffs', 'casino_1_total_payoff',
        'casino_2_num_dice_to_be_placed', 'casino_2_my_total_dice',
        'casino_2_total_other_dice', 'casino_2_total_players',
        'casino_2_my_dice_lead', 'casino_2_max_payoff', 'casino_2_num_payoffs',
        'casino_2_total_payoff', 'casino_3_num_dice_to_be_placed',
        'casino_3_my_total_dice', 'casino_3_total_other_dice',
        'casino_3_total_players', 'casino_3_my_dice_lead',
        'casino_3_max_payoff', 'casino_3_num_payoffs', 'casino_3_total_payoff',
        'casino_4_num_dice_to_be_placed', 'casino_4_my_total_dice',
        'casino_4_total_other_dice', 'casino_4_total_players',
        'casino_4_my_dice_lead', 'casino_4_max_payoff', 'casino_4_num_payoffs',
        'casino_4_total_payoff', 'casino_5_num_dice_to_be_placed',
        'casino_5_my_total_dice', 'casino_5_total_other_dice',
        'casino_5_total_players', 'casino_5_my_dice_lead',
        'casino_5_max_payoff', 'casino_5_num_payoffs', 'casino_5_total_payoff'
    ]

    def __init__(self):
        self._load_training_data()

        self.model = LogisticRegression(
            multi_class = "multinomial"
        )
        self.model.fit(
            self.training_data[self.x_vars].values,
            self.training_data.choice,
        )
        print("here"*10)

    def _load_file_and_create_feature_data_frame(
        self,
        filename,
    ) -> pd.DataFrame:
        with open(filename) as file_:
            lines = file_.readlines()

        rows = []

        for i, line in enumerate(lines):
            choice_, game_state = self._get_choice_and_game_state_from_line(line)
            features = self._get_features_from_game_state(game_state)

            features["choice"] = choice_
            features["index_"] = i
            
            rows.append(features)

        df = pd.DataFrame(rows)

        return df

class BinaryLogisticCasinoClassifierStrategy(MLBasedStrategy):

    def choose(
        self,
        game_state : GameState
    ) -> int:

        y_hats = [-1 for i in range(len(game_state.casinos))]

        for casino in game_state.casinos:
            features = self._get_features_from_game_state_and_casino(game_state, casino)

            feature_vector = array([i for i in features.values()]).reshape(1, -1)
            y_hat = self.model.predict_proba(feature_vector)

            y_hats[casino.id_] = y_hat[0][1]

        # print(y_hats)

        while 1:
            max_prob_casino_id = argmax(y_hats)

            dice = game_state.next_roll
            if max_prob_casino_id in dice:
                return max_prob_casino_id
            else:
                y_hats[max_prob_casino_id] = -1


    x_vars = [
        'my_dice_remaining',
        'total_other_dice_remaining',
        'casino_num_dice_to_be_placed',
        'casino_my_total_dice',
        'casino_total_other_dice',
        'casino_total_players',
        'casino_my_dice_lead',
        'casino_max_payoff',
        'casino_num_payoffs',
        'casino_total_payoff',
    ]

    def __init__(self):
        self._load_training_data()

        self.model = LogisticRegression()
        self.model.fit(
            self.training_data[self.x_vars].values,
            self.training_data.choice,
        )

    def _load_file_and_create_feature_data_frame(
        self,
        filename,
    ) -> pd.DataFrame:
        with open(filename) as file_:
            lines = file_.readlines()

        rows = []
        for i, line in enumerate(lines):
            choice_, game_state = self._get_choice_and_game_state_from_line(line)
            for casino in game_state.casinos:
                features = self._get_features_from_game_state_and_casino(game_state, casino)
                casino_id = casino.id_

                features["choice"] = int(choice_) == casino_id

                rows.append(features)

        df = pd.DataFrame(rows)
        return df

    @classmethod
    def _get_features_from_game_state_and_casino(
        cls,
        game_state,
        casino,
    ):
        my_id = game_state.next_player_id
        casino_id = casino.id_

        features = {
            "my_dice_remaining" : game_state.players[my_id].dice_remaining,
            "total_other_dice_remaining" : cls._calc_feature_total_other_dice_remaining(game_state, my_id),
            "casino_num_dice_to_be_placed" : sum([1 for i in game_state.next_roll if i == casino_id]),
            "casino_my_total_dice" : casino.placed_dice[my_id],
            "casino_total_other_dice" : sum([casino.placed_dice[id_] for id_ in range(len(game_state.players)) if not id_ == my_id]),
            "casino_total_players" : sum([casino.placed_dice[id_] > 0 for id_ in range(len(game_state.players))]),
            "casino_my_dice_lead" : cls._calc_feature_my_dice_lead(casino, my_id, len(game_state.players)),
            "casino_max_payoff" : casino.payouts[0],
            "casino_num_payoffs" : len(casino.payouts),
            "casino_total_payoff" : sum(casino.payouts),
        }

        return features