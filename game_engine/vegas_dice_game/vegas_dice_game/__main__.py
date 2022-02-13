import pandas as pd

from vegas_dice_game.game import Game


scores = []
for i in range(1000):
    my_game = Game()
    new_scores = my_game.play_game(verbosity=0)
    # print(new_scores)
    scores.append(new_scores)

df = pd.DataFrame(scores)
print(df.sum())