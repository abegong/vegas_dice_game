# import pandas as pd
# import json

# from vegas_dice_game.engine import GameState, Casino, Player
# from vegas_dice_game.strategy.base import Strategy

# class MLBasedStrategy(Strategy):


# with open("InputStrategy.log") as file_:
#     lines = file_.readlines()


# # In[3]:


# def get_choice_and_game_state_from_line(line):
#     choice_, game_state = line.split(' ', 1)

#     game_state_json = json.loads(game_state)
#     game_state = game_state_json
#     game_state["casinos"] = [Casino(**c) for c in game_state["casinos"]]
#     game_state["players"] = [Player(**p) for p in game_state["players"]]
#     game_state = GameState(**game_state)
    
#     return choice_, game_state

# # get_choice_and_game_state_from_line(lines[20])


# # In[4]:


# def calc_total_other_dice_remaining(
#     game_state,
#     my_id,
# ):
#     return sum([game_state.players[id_].dice_remaining for id_ in range(len(game_state.players)) if not id_ == my_id ])

# def calc_my_dice_lead(
#     casino,
#     my_id,
# ):
#     my_dice = casino.placed_dice[my_id]
#     max_other_dice = max([casino.placed_dice[id_] for id_ in range(len(game_state.players)) if not id_ == my_id ])
# #     print(casino)
# #     print(my_id)
# #     print(my_dice)
# #     print(max_other_dice)
#     return my_dice - max_other_dice


# # In[5]:


# def get_features_from_game_state(game_state):
#     my_id = game_state.next_player_id

#     features = {
#         "my_dice_remaining" : game_state.players[my_id].dice_remaining,
#         "total_other_dice_remaining" : calc_total_other_dice_remaining(game_state, my_id),
#     }
#     # print(general_features)

#     for casino in game_state.casinos:
#         casino_id = casino.id_
#         casino_level_features = {
#             f"casino_{casino_id}_num_dice_to_be_placed" : sum([1 for i in game_state.next_roll if i == casino_id]),
#             f"casino_{casino_id}_my_total_dice" : casino.placed_dice[my_id],
#             f"casino_{casino_id}_total_other_dice" : sum([casino.placed_dice[id_] for id_ in range(len(game_state.players)) if not id_ == my_id]),
#             f"casino_{casino_id}_total_players" : sum([casino.placed_dice[id_] > 0 for id_ in range(len(game_state.players))]),
#             f"casino_{casino_id}_my_dice_lead" : calc_my_dice_lead(casino, my_id),
#             f"casino_{casino_id}_max_payoff" : casino.payouts[0],
#             f"casino_{casino_id}_num_payoffs" : len(casino.payouts),
#             f"casino_{casino_id}_total_payoff" : sum(casino.payouts),
#         }
#     #     print(casino_level_features)

#         features = {**features, **casino_level_features}

#     return features


# # In[6]:


# rows = []
# for i, line in enumerate(lines):
#     choice_, game_state = get_choice_and_game_state_from_line(line)
#     features = get_features_from_game_state(game_state)

#     features["choice"] = choice_
#     features["index_"] = i
    
#     rows.append(features)


# # In[7]:


# df = pd.DataFrame(rows)


# # In[8]:


# df.choice.value_counts()


# # In[12]:


# x_vars = [
#     'my_dice_remaining', 'total_other_dice_remaining',
#    'casino_0_num_dice_to_be_placed', 'casino_0_my_total_dice',
#    'casino_0_total_other_dice', 'casino_0_total_players',
#    'casino_0_my_dice_lead', 'casino_0_max_payoff', 'casino_0_num_payoffs',
#    'casino_0_total_payoff', 'casino_1_num_dice_to_be_placed',
#    'casino_1_my_total_dice', 'casino_1_total_other_dice',
#    'casino_1_total_players', 'casino_1_my_dice_lead',
#    'casino_1_max_payoff', 'casino_1_num_payoffs', 'casino_1_total_payoff',
#    'casino_2_num_dice_to_be_placed', 'casino_2_my_total_dice',
#    'casino_2_total_other_dice', 'casino_2_total_players',
#    'casino_2_my_dice_lead', 'casino_2_max_payoff', 'casino_2_num_payoffs',
#    'casino_2_total_payoff', 'casino_3_num_dice_to_be_placed',
#    'casino_3_my_total_dice', 'casino_3_total_other_dice',
#    'casino_3_total_players', 'casino_3_my_dice_lead',
#    'casino_3_max_payoff', 'casino_3_num_payoffs', 'casino_3_total_payoff',
#    'casino_4_num_dice_to_be_placed', 'casino_4_my_total_dice',
#    'casino_4_total_other_dice', 'casino_4_total_players',
#    'casino_4_my_dice_lead', 'casino_4_max_payoff', 'casino_4_num_payoffs',
#    'casino_4_total_payoff', 'casino_5_num_dice_to_be_placed',
#    'casino_5_my_total_dice', 'casino_5_total_other_dice',
#    'casino_5_total_players', 'casino_5_my_dice_lead',
#    'casino_5_max_payoff', 'casino_5_num_payoffs', 'casino_5_total_payoff'
# ]


# # In[16]:


# from sklearn.linear_model import LogisticRegression

# model = LogisticRegression(
#     multi_class = "multinomial"
# )
# model.fit(df[x_vars], df.choice)


# # In[24]:


# # model.predict_proba(df[x_vars])
# y_hat = model.predict(df[x_vars])
# y_hat


# # In[ ]:


# model.get_params()


# # In[21]:


# # model.coef_


# # In[23]:


# model.score(df[x_vars], df.choice)


# # In[25]:


# pd.crosstab(y_hat, df.choice)


# # In[ ]:


# # decision_function(X)
# # Predict confidence scores for samples.
# # densify()
# # Convert coefficient matrix to dense array format.
# # fit(X, y[, sample_weight])
# # Fit the model according to the given training data.
# # get_params([deep])
# # Get parameters for this estimator.
# # predict(X)
# # Predict class labels for samples in X.
# # predict_log_proba(X)
# # Predict logarithm of probability estimates.
# # predict_proba(X)
# # Probability estimates.
# # score(X, y[, sample_weight])
# # Return the mean accuracy on the given test data and labels.
# # set_params(**params)
# # Set the parameters of this estimator.
# # sparsify()

