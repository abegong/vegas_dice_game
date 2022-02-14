import click
import random

@click.group()
def cli():
    pass

@click.command()
@click.option('--num_games', default=1000, help='Number of games to play.')
def simulate(num_games):
    import pandas as pd
    from vegas_dice_game.game import Game

    # strategies = ["RandomStrategy", "RandomStrategy", "RandomStrategy", "MLBasedStrategy"]
    strategies = ["BinaryLogisticCasinoClassifierStrategy", "MultinomialLogisticCasinoClassifierStrategy", "MultinomialLogisticCasinoClassifierStrategy", "BinaryLogisticCasinoClassifierStrategy"]
    # strategies = ["JonahsGreatStrategy", "JonahsGreatStrategy", "JonahsGreatStrategy", "BinaryLogisticCasinoClassifierStrategy"]

    scores = []
    for i in range(num_games):
        print("X"*80)
        # random.shuffle(strategies)
        my_game = Game(
            strategies = strategies
        )
        new_scores = my_game.play_game(verbosity=0)
        scores.append(new_scores)

    df = pd.DataFrame(scores)
    print(df.sum())

@click.command()
def play():
    import random
    from vegas_dice_game.game import Game

    strategies = ["BinaryLogisticCasinoClassifierStrategy", "BinaryLogisticCasinoClassifierStrategy", "BinaryLogisticCasinoClassifierStrategy", "InputStrategy"]
    random.shuffle(strategies)

    my_game = Game(
        strategies = strategies
    )
    new_scores = my_game.play_game()


cli.add_command(simulate)
cli.add_command(play)

if __name__ == '__main__':
    cli()